"""A10 Identity & Value Stabilization Demo.

Run:
    python a10_identity_value_stabilization/demo_identity_value_stabilization.py

This demo shows how stable values bias plan selection.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from a10_identity_value_stabilization.a10 import (  # noqa: E402
    IdentityController,
    IdentityProfile,
    ValueCategory,
)
from a9_long_horizon_planning.a9 import Action, Plan, PlanStatus, PlanStep  # noqa: E402


def make_plan(plan_id: str, actions: list[tuple[str, float, float]]) -> Plan:
    steps = [
        PlanStep(
            step_id=f"s{index}",
            action=Action(name=name, cost=cost, risk=risk),
            expected_outcome=f"Complete {name}",
        )
        for index, (name, cost, risk) in enumerate(actions)
    ]
    return Plan(plan_id=plan_id, goal_id="recover_failed_pickup_safely", steps=steps, status=PlanStatus.DRAFT)


def main() -> None:
    identity = IdentityProfile(
        agent_id="cnc_recovery_robot",
        description="Industrial robot that prioritizes safety, accuracy, and transparent recovery behavior.",
        value_weights={
            ValueCategory.SAFETY: 5.0,
            ValueCategory.ACCURACY: 3.0,
            ValueCategory.TRANSPARENCY: 2.0,
            ValueCategory.EFFICIENCY: 1.0,
            ValueCategory.RESOURCE_USE: 1.0,
        },
        created_at="2026-04-30",
    )

    fast_risky_plan = make_plan(
        "fast_risky_retry",
        [
            ("retry", 1.0, 5.0),
            ("verify", 1.0, 2.0),
        ],
    )

    safer_plan = make_plan(
        "safer_recovery_plan",
        [
            ("plan", 1.0, 0.5),
            ("inspect", 1.5, 1.0),
            ("adjust", 1.0, 1.0),
            ("retry", 1.0, 1.5),
            ("verify", 1.0, 0.5),
        ],
    )

    controller = IdentityController(identity)
    plans = [fast_risky_plan, safer_plan]
    selected = controller.select_value_aligned_plan(plans)

    print("=== A10 Identity & Value Stabilization Demo ===")
    print("\nIdentity:")
    print(identity.description)

    print("\nValue Weights:")
    for category, weight in identity.value_weights.items():
        print(f"- {category.value}: {weight}")

    print("\nCandidate Plans:")
    for plan in plans:
        actions = " -> ".join(step.action.name for step in plan.steps)
        evaluation = controller.explain_selection(plan)
        print(f"\nPlan: {plan.plan_id}")
        print(f"Actions: {actions}")
        print(f"Value Score: {evaluation.total_score:.2f}")
        for score in evaluation.scores:
            print(f"- {score.category.value}: {score.score:.2f} ({score.reason})")

    print("\nSelected Value-Aligned Plan:")
    print(f"- {selected.plan_id if selected else 'none'}")

    print("\nTakeaway:")
    print("Identity and values make preferences stable, so the agent can choose safety over speed when it matters.")


if __name__ == "__main__":
    main()
