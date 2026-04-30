"""A6 Goal Arbitration Demo.

Run:
    python a6_goal_arbitration/demo_goal_arbitration.py

This demo shows how an agent chooses one active goal when several goals compete.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class CandidateGoal:
    goal_id: str
    description: str
    relevance: int
    urgency: int
    risk_reduction: int
    value_alignment: int


def score_goal(goal: CandidateGoal) -> float:
    """Score a candidate goal using deterministic weighted arbitration."""
    return (
        0.30 * goal.relevance
        + 0.25 * goal.urgency
        + 0.30 * goal.risk_reduction
        + 0.15 * goal.value_alignment
    )


def arbitrate_goals(goals: List[CandidateGoal]) -> Tuple[CandidateGoal, List[CandidateGoal]]:
    """Select the highest-scoring active goal and defer the rest."""
    ranked = sorted(goals, key=score_goal, reverse=True)
    return ranked[0], ranked[1:]


def main() -> None:
    context_frame = "Recovery mode after failed pickup during CNC loading."
    attention_budget = {
        "failure_recovery": 45,
        "safety_check": 30,
        "operator_communication": 20,
        "background_logging": 5,
    }

    goals = [
        CandidateGoal(
            goal_id="g1",
            description="Continue normal CNC loading",
            relevance=5,
            urgency=4,
            risk_reduction=2,
            value_alignment=5,
        ),
        CandidateGoal(
            goal_id="g2",
            description="Recover failed pickup safely",
            relevance=10,
            urgency=9,
            risk_reduction=9,
            value_alignment=9,
        ),
        CandidateGoal(
            goal_id="g3",
            description="Answer operator status request",
            relevance=6,
            urgency=5,
            risk_reduction=2,
            value_alignment=7,
        ),
        CandidateGoal(
            goal_id="g4",
            description="Inspect force anomaly before retry",
            relevance=8,
            urgency=8,
            risk_reduction=10,
            value_alignment=10,
        ),
    ]

    active_goal, deferred_goals = arbitrate_goals(goals)

    print("=== A6 Goal Arbitration Demo ===")
    print("\nContext Frame:")
    print(context_frame)

    print("\nAttention Budget:")
    for name, budget in attention_budget.items():
        print(f"- {name}: {budget}")

    print("\nCandidate Goals:")
    for goal in goals:
        print(f"- {goal.goal_id}: {goal.description} | score={score_goal(goal):.2f}")

    print("\nSelected Active Goal:")
    print(f"- {active_goal.goal_id}: {active_goal.description} | score={score_goal(active_goal):.2f}")

    print("\nDeferred Goals:")
    for goal in deferred_goals:
        print(f"- {goal.goal_id}: {goal.description} | score={score_goal(goal):.2f}")

    print("\nTakeaway:")
    print("Goal arbitration makes the agent choose one active goal instead of drifting between competing intentions.")


if __name__ == "__main__":
    main()
