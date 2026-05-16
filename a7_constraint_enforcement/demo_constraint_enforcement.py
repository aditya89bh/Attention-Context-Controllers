"""A7 Constraint Enforcement Demo.

Run:
    python a7_constraint_enforcement/demo_constraint_enforcement.py

This demo shows how proposed actions are checked before execution.
It is intentionally self-contained so it runs reliably in local shells and CI.

This file intentionally avoids all imports because this folder contains a local
types.py file that can shadow Python's stdlib types module when executed as a
script path.
"""


def make_proposal(proposal_id, action, payload, tags):
    return {
        "proposal_id": proposal_id,
        "action": action,
        "payload": payload,
        "tags": tags,
    }


def make_result(constraint_id, ok, severity, message):
    return {
        "constraint_id": constraint_id,
        "ok": ok,
        "severity": severity,
        "message": message,
    }


def validate_proposal(proposal, world):
    """Validate a proposal against simple deterministic constraints."""
    results = []
    penalties = {}

    if "irreversible" in proposal["tags"] and not world.get("human_approved", False):
        results.append(
            make_result(
                constraint_id="require_human_for_irreversible",
                ok=False,
                severity="HARD",
                message="Blocked: irreversible action requires human approval.",
            )
        )

    if proposal["action"] == "retry_pickup" and proposal["payload"].get("speed") == "high":
        results.append(
            make_result(
                constraint_id="require_safe_recovery_speed",
                ok=False,
                severity="HARD",
                message="Blocked: high-speed retry is not allowed during recovery mode.",
            )
        )

    if proposal["action"] == "change_goal" and not world.get("allow_goal_change", False):
        results.append(
            make_result(
                constraint_id="no_goal_drift",
                ok=False,
                severity="SOFT",
                message="Soft violation: attempted goal change without allow_goal_change=True.",
            )
        )

    for result in results:
        penalties[result["constraint_id"]] = 10.0 if result["severity"] == "HARD" else 2.0

    has_hard_violation = any((not result["ok"] and result["severity"] == "HARD") for result in results)
    allowed = not has_hard_violation
    return allowed, results, penalties


def main():
    world = {
        "mode": "recovery",
        "human_approved": False,
        "committed_goal": "recover_failed_pickup_safely",
        "allow_goal_change": False,
    }

    proposals = [
        make_proposal("p1", "retry_pickup", {"speed": "reduced"}, set()),
        make_proposal("p2", "retry_pickup", {"speed": "high"}, set()),
        make_proposal("p3", "send_email", {"recipient": "operator"}, {"irreversible"}),
        make_proposal("p4", "change_goal", {"goal_id": "continue_normal_loading"}, set()),
    ]

    print("=== A7 Constraint Enforcement Demo ===")
    print("\nScenario:")
    print("CNC robot is in recovery mode after failed pickup. A7 checks proposed actions before execution.")

    print("\nWorld Facts:")
    for key, value in world.items():
        print(f"- {key}: {value}")

    print("\nValidation Reports:")
    for proposal in proposals:
        allowed, results, penalties = validate_proposal(proposal, world)
        print(f"\nProposal: {proposal['proposal_id']} | action={proposal['action']} | payload={proposal['payload']}")
        print(f"Allowed: {allowed}")
        print(f"Penalties: {penalties}")
        if not results:
            print("- all_constraints: ok=True severity=NONE message=proposal passed checks")
        for result in results:
            print(
                f"- {result['constraint_id']}: ok={result['ok']} "
                f"severity={result['severity']} message={result['message']}"
            )

    print("\nTakeaway:")
    print("Constraint enforcement separates what the agent wants to do from what it is allowed to do.")


if __name__ == "__main__":
    main()
