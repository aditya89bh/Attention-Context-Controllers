"""A3 Salience Memory Access Demo.

Run:
    python a3_salience_memory_access/demo_salience_memory_access.py

This demo shows how task-relevant memories are selected and noisy memories are ignored.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Memory:
    memory_id: str
    content: str
    relevance: int
    recency: int
    risk_connection: int
    goal_fit: int


def score_memory(memory: Memory) -> float:
    """Score memory salience using deterministic weighted features."""
    return (
        0.35 * memory.relevance
        + 0.20 * memory.recency
        + 0.25 * memory.risk_connection
        + 0.20 * memory.goal_fit
    )


def select_salient_memories(memories: List[Memory], threshold: float = 6.0) -> Tuple[List[Tuple[Memory, float]], List[Tuple[Memory, float]]]:
    """Split memories into selected and ignored groups."""
    scored = [(memory, score_memory(memory)) for memory in memories]
    scored.sort(key=lambda item: item[1], reverse=True)

    selected = [(memory, score) for memory, score in scored if score >= threshold]
    ignored = [(memory, score) for memory, score in scored if score < threshold]
    return selected, ignored


def main() -> None:
    context_frame = "Recovery mode after failed pickup during CNC loading."
    active_goal = "recover failed pickup safely"

    memories = [
        Memory(
            memory_id="m1",
            content="Tray drift happened yesterday during CNC loading.",
            relevance=10,
            recency=9,
            risk_connection=8,
            goal_fit=10,
        ),
        Memory(
            memory_id="m2",
            content="Previous pickup retry succeeded after applying a small tray offset.",
            relevance=9,
            recency=7,
            risk_connection=7,
            goal_fit=9,
        ),
        Memory(
            memory_id="m3",
            content="Operator prefers short status updates during recovery events.",
            relevance=6,
            recency=6,
            risk_connection=2,
            goal_fit=5,
        ),
        Memory(
            memory_id="m4",
            content="Weekly maintenance log mentioned cafeteria network outage.",
            relevance=1,
            recency=5,
            risk_connection=1,
            goal_fit=1,
        ),
        Memory(
            memory_id="m5",
            content="Old calibration note from six months ago.",
            relevance=3,
            recency=1,
            risk_connection=2,
            goal_fit=2,
        ),
    ]

    selected, ignored = select_salient_memories(memories)

    print("=== A3 Salience Memory Access Demo ===")
    print("\nContext Frame:")
    print(context_frame)
    print("\nActive Goal:")
    print(active_goal)

    print("\nMemory Candidates:")
    for memory in memories:
        print(f"- {memory.memory_id}: {memory.content}")

    print("\nSelected Memories:")
    for memory, score in selected:
        print(f"- {memory.memory_id}: score={score:.2f} | {memory.content}")

    print("\nIgnored Memories:")
    for memory, score in ignored:
        print(f"- {memory.memory_id}: score={score:.2f} | {memory.content}")

    print("\nTakeaway:")
    print("Memory becomes useful only when salience filters what matters for the current goal.")


if __name__ == "__main__":
    main()
