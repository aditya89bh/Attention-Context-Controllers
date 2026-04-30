"""A5 Interrupt / Task Switching Demo.

Run:
    python a5_interrupt_task_switching/demo_interrupt_task_switching.py

This demo shows when an agent should stay focused, pause, or switch tasks.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InterruptSignal:
    name: str
    urgency: int
    risk: int
    relevance: int
    description: str


@dataclass(frozen=True)
class SwitchDecision:
    decision: str
    reason: str
    priority_score: float


def evaluate_interrupt(signal: InterruptSignal, current_commitment: int) -> SwitchDecision:
    """Decide whether an interrupt should override current focus."""
    priority_score = (0.4 * signal.urgency) + (0.4 * signal.risk) + (0.2 * signal.relevance)
    commitment_resistance = current_commitment * 0.6

    if priority_score >= commitment_resistance + 2:
        return SwitchDecision(
            decision="switch_now",
            reason=f"{signal.name} has high risk/urgency relative to current commitment.",
            priority_score=priority_score,
        )

    if priority_score >= commitment_resistance:
        return SwitchDecision(
            decision="pause_and_check",
            reason=f"{signal.name} is important enough to pause and inspect before continuing.",
            priority_score=priority_score,
        )

    return SwitchDecision(
        decision="stay_focused",
        reason=f"{signal.name} does not justify interrupting the active task.",
        priority_score=priority_score,
    )


def main() -> None:
    current_task = "recover failed pickup during CNC loading"
    current_commitment = 8

    signals = [
        InterruptSignal(
            name="operator_status_request",
            urgency=5,
            risk=1,
            relevance=6,
            description="Operator asks what happened.",
        ),
        InterruptSignal(
            name="force_sensor_spike",
            urgency=9,
            risk=10,
            relevance=9,
            description="Force sensor spike detected near gripper.",
        ),
        InterruptSignal(
            name="background_log_update",
            urgency=1,
            risk=1,
            relevance=1,
            description="Unrelated maintenance log update arrives.",
        ),
    ]

    print("=== A5 Interrupt / Task Switching Demo ===")
    print("\nCurrent Task:")
    print(current_task)
    print(f"Current Commitment Strength: {current_commitment}")

    print("\nInterrupt Decisions:")
    for signal in signals:
        decision = evaluate_interrupt(signal, current_commitment)
        print(f"\nSignal: {signal.name}")
        print(f"Description: {signal.description}")
        print(f"Priority Score: {decision.priority_score:.2f}")
        print(f"Decision: {decision.decision}")
        print(f"Reason: {decision.reason}")

    print("\nTakeaway:")
    print("Interrupt control balances focus against urgent risk, so the agent is neither brittle nor distractible.")


if __name__ == "__main__":
    main()
