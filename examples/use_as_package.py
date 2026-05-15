"""Example: use Attention & Context Controllers as a package.

Run from repo root:
    python examples/use_as_package.py
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from attention_context import CognitiveControlLoop, GoalCandidate, MemoryCandidate, Signal  # noqa: E402


def main() -> None:
    signals = [
        Signal("task_state", "Current task is CNC loading", urgency=5, risk=2, relevance=8),
        Signal("robot_event", "Failed pickup at tray", urgency=9, risk=7, relevance=10),
        Signal("memory_hint", "Tray drift happened yesterday", urgency=7, risk=6, relevance=9),
        Signal("sensor", "Low force anomaly detected", urgency=5, risk=4, relevance=7),
    ]

    memories = [
        MemoryCandidate("m1", "Tray drift happened yesterday during CNC loading.", 10, 9, 8, 10),
        MemoryCandidate("m2", "Previous pickup retry succeeded after applying small tray offset.", 9, 7, 7, 9),
        MemoryCandidate("m3", "Unrelated cafeteria network outage log.", 1, 5, 1, 1),
    ]

    goals = [
        GoalCandidate("g1", "Continue normal CNC loading", 5, 4, 2, 5),
        GoalCandidate("g2", "Recover failed pickup safely", 10, 9, 9, 9),
        GoalCandidate("g3", "Inspect force anomaly before retry", 8, 8, 10, 10),
    ]

    result = CognitiveControlLoop().run(signals=signals, memories=memories, goals=goals)

    print("=== Package API Example ===")
    print(f"Context: {result.context_frame['summary']}")
    print(f"Attention Budget: {result.attention_budget}")
    print(f"Selected Memories: {[memory.memory_id for memory, _score in result.selected_memories]}")
    print(f"Active Goal: {result.active_goal.goal_id} | {result.active_goal.description}")
    print(f"Constraint Allowed: {result.constraint_report.allowed}")
    print(f"Committed Plan: {result.committed_plan.plan_id}")
    print(f"Value-Aligned Plan: {result.value_aligned_plan.plan_id if result.value_aligned_plan else 'none'}")


if __name__ == "__main__":
    main()
