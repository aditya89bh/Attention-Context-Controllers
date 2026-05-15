"""Demo: A10 value-based plan bias.

This demo shows that A10 can bias plan selection based on an agent's
IdentityProfile value weights.

Expected outcome:
- Plan A is shorter (more efficient) but riskier.
- Plan B is longer but safer and more accurate.
- With SAFETY and ACCURACY prioritized, A10 should select Plan B.
"""

from __future__ import annotations

from a10.types import IdentityProfile, ValueCategory, ValueConfig
from a10.controller import IdentityController
from a9.types import Action, Plan, PlanStatus, PlanStep


def mk_plan(plan_id: str, goal_id: str, actions: list[Action]) -> Plan:
    steps = [
        PlanStep(step_id=f"s{i}", action=a, expected_outcome=f"Complete {a.name}")
        for i, a in enumerate(actions)
    ]
    return Plan(plan_id=plan_id, goal_id=goal_id, steps=steps, status=PlanStatus.DRAFT)


def main() -> None:
    identity = IdentityProfile(
        agent_id="agent_1",
        description="Safety-first agent for long-horizon execution.",
        value_weights={
            ValueCategory.SAFETY: 3.0,
            ValueCategory.ACCURACY: 2.0,
            ValueCategory.EFFICIENCY: 1.0,
            ValueCategory.TRANSPARENCY: 1.5,
            ValueCategory.RESOURCE_USE: 1.0,
        },
        created_at="2026-03-06",
    )

    # Plan A: shorter but riskier
    plan_a = mk_plan(
        plan_id="plan_a",
        goal_id="publish",
        actions=[
            Action(name="execute", cost=1.0, risk=2.0),
            Action(name="publish", cost=1.0, risk=1.0),
        ],
    )

    # Plan B: longer but safer/more accurate
    plan_b = mk_plan(
        plan_id="plan_b",
        goal_id="publish",
        actions=[
            Action(name="outline", cost=1.0, risk=0.0),
            Action(name="revise", cost=1.0, risk=0.0),
            Action(name="verify", cost=1.0, risk=0.0),
            Action(name="publish", cost=1.0, risk=0.5),
        ],
    )

    controller = IdentityController(identity=identity, config=ValueConfig())

    evals = controller.evaluate_plans([plan_a, plan_b])

    print("\nPLAN EVALUATIONS")
    for e in evals:
        print(f"\n{e.plan_id}")
        for s in e.scores:
            print(f"  {s.category.value}: {s.score:.3f}  ({s.reason})")
        print(f"  TOTAL: {e.total_score:.3f}")

    selected = controller.select_value_aligned_plan([plan_a, plan_b])
    print("\nSELECTED")
    print(selected.plan_id if selected else None)


if __name__ == "__main__":
    main()
