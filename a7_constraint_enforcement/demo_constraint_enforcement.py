"""A7 Constraint Enforcement Demo.

Run:
    python a7_constraint_enforcement/demo_constraint_enforcement.py

This demo shows how unsafe or inconsistent action proposals are blocked before execution.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from a7_constraint_enforcement import (  # noqa: E402
    Commitment,
    ConsistencyController,
    DecisionProposal,
    DecisionType,
    EnforcementMode,
    WorldState,
    constraint_no_contradict_commitment,
    constraint_no_goal_drift,
    constraint_require_human_for_irreversible,
)


def main() -> None:
    controller = ConsistencyController(mode=EnforcementMode.STRICT)
    controller.add_constraint(constraint_require_human_for_irreversible())
    controller.add_constraint(constraint_no_contradict_commitment("no_high_speed_retry"))
    controller.add_constraint(constraint_no_goal_drift())

    world = WorldState(
        facts={
            "human_approved": False,
            "committed_goal": "recover_failed_pickup_safely",
            "allow_goal_change": False,
        }
    )
    controller.commit(
        world,
        Commitment(
            commitment_id="c1",
            description="Do not retry pickup at high speed during recovery mode.",
            tags={"no_high_speed_retry"},
        ),
    )

    proposals = [
        DecisionProposal(
            decision_id="p1",
            decision_type=DecisionType.ACTION,
            payload={"action": "retry_pickup", "speed": "reduced"},
            tags=set(),
        ),
        DecisionProposal(
            decision_id="p2",
            decision_type=DecisionType.ACTION,
            payload={"action": "send_email"},
            tags={"irreversible"},
        ),
        DecisionProposal(
            decision_id="p3",
            decision_type=DecisionType.GOAL_SELECT,
            payload={"goal_id": "continue_normal_loading"},
            tags=set(),
        ),
    ]

    print("=== A7 Constraint Enforcement Demo ===")
    print("\nScenario:")
    print("CNC robot is in recovery mode after failed pickup. A7 checks proposed actions before execution.")

    print("\nWorld Facts:")
    for key, value in world.facts.items():
        print(f"- {key}: {value}")

    print("\nActive Commitments:")
    for commitment in world.commitments.values():
        print(f"- {commitment.commitment_id}: {commitment.description} tags={sorted(commitment.tags)}")

    print("\nValidation Reports:")
    for proposal in proposals:
        report = controller.validate(proposal, world)
        controller.apply_if_allowed(report, world)
        print(f"\nProposal: {proposal.decision_id} | {proposal.decision_type.value} | {proposal.payload}")
        print(f"Allowed: {report.allowed}")
        print(f"Penalties: {report.penalties}")
        for result in report.results:
            print(f"- {result.constraint_id}: ok={result.ok} severity={result.severity} message={result.message}")

    print("\nTakeaway:")
    print("Constraint enforcement separates what the agent wants to do from what it is allowed to do.")


if __name__ == "__main__":
    main()
