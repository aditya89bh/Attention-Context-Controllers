"""A4 Temporal Context Demo.

Run:
    python a4_temporal_context/demo_temporal_context.py

This demo shows how an agent separates past memory, present state, and future simulation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TemporalSignal:
    label: str
    content: str
    time_mode: str


@dataclass(frozen=True)
class TemporalContext:
    past: List[str]
    present: List[str]
    future: List[str]


def build_temporal_context(signals: List[TemporalSignal]) -> TemporalContext:
    """Group signals into past, present, and future context."""
    past = [signal.content for signal in signals if signal.time_mode == "past"]
    present = [signal.content for signal in signals if signal.time_mode == "present"]
    future = [signal.content for signal in signals if signal.time_mode == "future"]

    return TemporalContext(past=past, present=present, future=future)


def main() -> None:
    signals = [
        TemporalSignal(
            label="memory",
            content="Tray drift happened yesterday during CNC loading.",
            time_mode="past",
        ),
        TemporalSignal(
            label="memory",
            content="Previous retry succeeded after applying a small tray offset.",
            time_mode="past",
        ),
        TemporalSignal(
            label="robot_state",
            content="Current pickup attempt failed at tray position.",
            time_mode="present",
        ),
        TemporalSignal(
            label="sensor",
            content="Low force anomaly is currently visible.",
            time_mode="present",
        ),
        TemporalSignal(
            label="simulation",
            content="Retry may succeed if tray offset is adjusted before next pickup.",
            time_mode="future",
        ),
        TemporalSignal(
            label="simulation",
            content="If force anomaly increases, pause and request operator inspection.",
            time_mode="future",
        ),
    ]

    temporal_context = build_temporal_context(signals)

    print("=== A4 Temporal Context Demo ===")
    print("\nScenario:")
    print("CNC robot failed pickup during loading. The agent must separate memory, current facts, and possible next actions.")

    print("\nRaw Temporal Signals:")
    for signal in signals:
        print(f"- [{signal.time_mode}] {signal.label}: {signal.content}")

    print("\nTemporal Context:")
    print("Past:")
    for item in temporal_context.past:
        print(f"- {item}")

    print("\nPresent:")
    for item in temporal_context.present:
        print(f"- {item}")

    print("\nFuture:")
    for item in temporal_context.future:
        print(f"- {item}")

    print("\nTakeaway:")
    print("Temporal context prevents the agent from confusing memory, current state, and prediction.")


if __name__ == "__main__":
    main()
