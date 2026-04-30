"""A8 Self-Monitoring Demo.

Run:
    python a8_self_monitoring/demo_self_monitoring.py

This demo shows how an agent detects loops, thrashing, and repeated violations from behavior traces.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from a8_self_monitoring.controller import SelfMonitoringController  # noqa: E402
from a8_self_monitoring.types import MonitorConfig  # noqa: E402


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

    controller = SelfMonitoringController(
        MonitorConfig(
            window=12,
            loop_repetition_threshold=4,
            thrash_switch_threshold=6,
            violation_repeat_threshold=3,
        )
    )
    report = controller.analyze(events)

    print("=== A8 Self-Monitoring Demo ===")
    print("\nScenario:")
    print("The robot repeatedly retries pickup and repeatedly hits the same safety constraint.")

    print("\nBehavior Events:")
    for event in events:
        print(f"- {event['type']}: {event.get('payload')}")

    print("\nDetected Issues:")
    for issue in report.issues:
        print(f"- {issue.issue_type.value} | {issue.severity.value} | {issue.message}")

    print("\nSuggested Interventions:")
    for intervention in report.interventions:
        print(f"- {intervention.name}: {intervention.reason}")

    print("\nReport Notes:")
    for key, value in report.notes.items():
        print(f"- {key}: {value}")

    print("\nTakeaway:")
    print("Self-monitoring lets the agent notice when behavior is unstable instead of blindly continuing.")


if __name__ == "__main__":
    main()
