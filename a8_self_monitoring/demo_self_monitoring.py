"""A8 Self-Monitoring Demo.

Run:
    python a8_self_monitoring/demo_self_monitoring.py

This demo shows how an agent detects loops and repeated violations from behavior traces.
It is intentionally self-contained so it runs reliably in local shells and CI.
"""

from __future__ import annotations

from collections import Counter


def event_signature(event: dict) -> str:
    payload = event.get("payload") or {}
    action = payload.get("action")
    if action:
        return f"action:{action}"
    return f"event:{event.get('type', 'unknown')}"


def detect_issues(events: list[dict], loop_threshold: int = 4, violation_threshold: int = 3) -> tuple[list[str], list[str]]:
    """Detect repeated actions and repeated blocked constraints."""
    signatures = [event_signature(event) for event in events]
    signature_counts = Counter(signatures)

    issues: list[str] = []
    interventions: list[str] = []

    for signature, count in signature_counts.items():
        if count >= loop_threshold:
            issues.append(f"LOOP | MEDIUM | Loop detected: {signature} repeated {count} times.")
            interventions.append(f"pause_and_replan: Loop detected on {signature}.")

    violations: list[str] = []
    for event in events:
        if event.get("type") != "proposal_blocked":
            continue
        for result in event.get("results", []):
            if not result.get("ok", True):
                violations.append(result.get("constraint_id", "unknown"))

    violation_counts = Counter(violations)
    for constraint_id, count in violation_counts.items():
        if count >= violation_threshold:
            issues.append(f"REPEATED_VIOLATION | MEDIUM | Repeated violation: {constraint_id} triggered {count} times.")
            interventions.append(
                f"escalate_or_adjust: Repeatedly hitting {constraint_id}. Ask for approval or revise strategy."
            )

    return issues, interventions


def main() -> None:
    events = [
        {"type": "proposal_accepted", "proposal": "p1", "payload": {"action": "retry_pickup"}},
        {"type": "proposal_accepted", "proposal": "p2", "payload": {"action": "retry_pickup"}},
        {"type": "proposal_accepted", "proposal": "p3", "payload": {"action": "retry_pickup"}},
        {"type": "proposal_accepted", "proposal": "p4", "payload": {"action": "retry_pickup"}},
        {
            "type": "proposal_blocked",
            "proposal": "p5",
            "payload": {"action": "high_speed_retry"},
            "results": [
                {
                    "constraint_id": "require_safe_recovery_speed",
                    "ok": False,
                    "severity": "HARD",
                    "message": "High speed retry blocked during recovery mode.",
                }
            ],
        },
        {
            "type": "proposal_blocked",
            "proposal": "p6",
            "payload": {"action": "high_speed_retry"},
            "results": [
                {
                    "constraint_id": "require_safe_recovery_speed",
                    "ok": False,
                    "severity": "HARD",
                    "message": "High speed retry blocked during recovery mode.",
                }
            ],
        },
        {
            "type": "proposal_blocked",
            "proposal": "p7",
            "payload": {"action": "high_speed_retry"},
            "results": [
                {
                    "constraint_id": "require_safe_recovery_speed",
                    "ok": False,
                    "severity": "HARD",
                    "message": "High speed retry blocked during recovery mode.",
                }
            ],
        },
    ]

    issues, interventions = detect_issues(events)

    print("=== A8 Self-Monitoring Demo ===")
    print("\nScenario:")
    print("The robot repeatedly retries pickup and repeatedly hits the same safety constraint.")

    print("\nBehavior Events:")
    for event in events:
        print(f"- {event['type']}: {event.get('payload')}")

    print("\nDetected Issues:")
    for issue in issues:
        print(f"- {issue}")

    print("\nSuggested Interventions:")
    for intervention in interventions:
        print(f"- {intervention}")

    print("\nReport Notes:")
    print(f"- window: 12")
    print(f"- events_seen: {len(events)}")

    print("\nTakeaway:")
    print("Self-monitoring lets the agent notice when behavior is unstable instead of blindly continuing.")


if __name__ == "__main__":
    main()
