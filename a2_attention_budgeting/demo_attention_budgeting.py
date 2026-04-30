"""A2 Attention Budgeting Demo.

Run:
    python a2_attention_budgeting/demo_attention_budgeting.py

This demo shows how limited reasoning budget is allocated across competing concerns.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Concern:
    name: str
    relevance: int
    urgency: int
    risk: int


def allocate_attention_budget(concerns: List[Concern], total_budget: int = 100) -> Dict[str, int]:
    """Allocate attention budget using deterministic weighted scoring."""
    raw_scores: Dict[str, float] = {}

    for concern in concerns:
        score = (
            0.45 * concern.relevance
            + 0.30 * concern.urgency
            + 0.25 * concern.risk
        )
        raw_scores[concern.name] = score

    total_score = sum(raw_scores.values()) or 1.0
    allocation = {
        name: int(round((score / total_score) * total_budget))
        for name, score in raw_scores.items()
    }

    # Fix rounding drift so total equals total_budget.
    drift = total_budget - sum(allocation.values())
    if drift != 0:
        top_name = max(allocation, key=allocation.get)
        allocation[top_name] += drift

    return dict(sorted(allocation.items(), key=lambda item: item[1], reverse=True))


def main() -> None:
    context_frame = "Recovery mode after failed pickup during CNC loading."
    concerns = [
        Concern(name="failure_recovery", relevance=10, urgency=9, risk=8),
        Concern(name="safety_check", relevance=8, urgency=8, risk=10),
        Concern(name="operator_communication", relevance=6, urgency=5, risk=2),
        Concern(name="background_logging", relevance=2, urgency=1, risk=1),
    ]

    budget = allocate_attention_budget(concerns)

    print("=== A2 Attention Budgeting Demo ===")
    print("\nContext Frame:")
    print(context_frame)

    print("\nCompeting Concerns:")
    for concern in concerns:
        print(
            f"- {concern.name}: relevance={concern.relevance} "
            f"urgency={concern.urgency} risk={concern.risk}"
        )

    print("\nAttention Budget:")
    for name, value in budget.items():
        print(f"- {name}: {value}")

    print("\nTakeaway:")
    print("Attention is finite. The agent should not reason equally about everything.")


if __name__ == "__main__":
    main()
