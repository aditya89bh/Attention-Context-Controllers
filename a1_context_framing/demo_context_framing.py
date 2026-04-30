"""A1 Context Framing Demo.

Run:
    python a1_context_framing/demo_context_framing.py

This demo shows how raw robot/task signals become a compact reasoning frame.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Signal:
    source: str
    content: str
    urgency: int
    risk: int


@dataclass(frozen=True)
class ContextFrame:
    mode: str
    task: str
    summary: str
    focus: List[str]


def build_context_frame(current_task: str, signals: List[Signal]) -> ContextFrame:
    """Build a simple deterministic context frame from raw signals."""
    has_failed_pickup = any("failed pickup" in signal.content.lower() for signal in signals)
    has_tray_drift_memory = any("tray drift" in signal.content.lower() for signal in signals)
    has_operator_status = any("status" in signal.content.lower() for signal in signals)

    if has_failed_pickup:
        mode = "recovery"
        summary = f"Recovery mode after failed pickup during {current_task}."
    else:
        mode = "normal_execution"
        summary = f"Normal execution mode for {current_task}."

    focus = ["recover failed pickup"] if has_failed_pickup else ["continue task"]

    if has_tray_drift_memory:
        focus.append("check tray pose drift")
    if has_operator_status:
        focus.append("prepare operator status update")

    return ContextFrame(
        mode=mode,
        task=current_task,
        summary=summary,
        focus=focus,
    )


def main() -> None:
    current_task = "CNC loading"
    signals = [
        Signal(source="task_state", content="Current task is CNC loading", urgency=5, risk=2),
        Signal(source="robot_event", content="Failed pickup at tray", urgency=9, risk=7),
        Signal(source="operator", content="Operator asks for status", urgency=6, risk=1),
        Signal(source="memory_hint", content="Tray drift happened yesterday", urgency=7, risk=6),
        Signal(source="sensor", content="Low force anomaly detected", urgency=5, risk=4),
    ]

    frame = build_context_frame(current_task=current_task, signals=signals)

    print("=== A1 Context Framing Demo ===")
    print("\nScenario:")
    print("CNC robot failed pickup during loading.\n")

    print("Raw Signals:")
    for signal in signals:
        print(f"- [{signal.source}] {signal.content} | urgency={signal.urgency} risk={signal.risk}")

    print("\nContext Frame:")
    print(f"Mode: {frame.mode}")
    print(f"Task: {frame.task}")
    print(f"Summary: {frame.summary}")
    print("Focus:")
    for item in frame.focus:
        print(f"- {item}")

    print("\nTakeaway:")
    print("Context framing turns raw signals into a useful reasoning frame.")


if __name__ == "__main__":
    main()
