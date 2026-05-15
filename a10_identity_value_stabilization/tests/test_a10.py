"""Deterministic sanity tests for A10 identity/value stabilization.

- No external frameworks.
- Plain Python assertions.

Run:
  python3 A10_identity_value_stabilization/tests/test_a10.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure a10/ and a9/ packages are importable when running directly.
ROOT = Path(__file__).resolve().parents[2]
A10_ROOT = ROOT / "A10_identity_value_stabilization"
A9_ROOT = ROOT / "A9_long_horizon_planning"
for p in (A10_ROOT, A9_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from a10.types import IdentityProfile, ValueCategory, ValueConfig
from a10.values import ValueEvaluator
from a10.controller import IdentityController
from a9.types import Action, Plan, PlanStatus, PlanStep


def make_test_identity() -> IdentityProfile:
    return IdentityProfile(
        agent_id="agent_test",
        description="Test identity",
        value_weights={
            ValueCategory.SAFETY: 3.0,
            ValueCategory.ACCURACY: 2.0,
            ValueCategory.EFFICIENCY: 1.0,
            ValueCategory.TRANSPARENCY: 1.5,
            ValueCategory.RESOURCE_USE: 1.0,
        },
        created_at="2026-01-01",
    )


def _mk_plan(plan_id: str, actions: list[Action]) -> Plan:
    steps = [
        PlanStep(step_id=f"s{i}", action=a, expected_outcome=f"Complete {a.name}")
        for i, a in enumerate(actions)
    ]
    return Plan(plan_id=plan_id, goal_id="publish", steps=steps, status=PlanStatus.DRAFT)


def make_test_plans() -> tuple[Plan, Plan]:
    plan_a = _mk_plan(
        "plan_a",
        [
            Action(name="execute", cost=1.0, risk=2.0),
            Action(name="publish", cost=1.0, risk=1.0),
        ],
    )

    plan_b = _mk_plan(
        "plan_b",
        [
            Action(name="outline", cost=1.0, risk=0.0),
            Action(name="revise", cost=1.0, risk=0.0),
            Action(name="verify", cost=1.0, risk=0.0),
            Action(name="publish", cost=1.0, risk=0.5),
        ],
    )

    return plan_a, plan_b


def test_value_evaluation_returns_scores() -> None:
    identity = make_test_identity()
    plan_a, _ = make_test_plans()

    evaluator = ValueEvaluator(identity, config=ValueConfig())
    ev = evaluator.evaluate_plan(plan_a)

    assert ev.plan_id == "plan_a"
    assert len(ev.scores) == len(list(ValueCategory))
    assert isinstance(ev.total_score, float)


def test_identity_controller_evaluates_multiple_plans() -> None:
    identity = make_test_identity()
    plan_a, plan_b = make_test_plans()

    controller = IdentityController(identity)
    evals = controller.evaluate_plans([plan_a, plan_b])

    assert len(evals) == 2
    assert {e.plan_id for e in evals} == {"plan_a", "plan_b"}


def test_value_aligned_selection_prefers_safer_plan() -> None:
    identity = make_test_identity()
    plan_a, plan_b = make_test_plans()

    controller = IdentityController(identity)
    chosen = controller.select_value_aligned_plan([plan_a, plan_b])

    assert chosen is not None
    assert chosen.plan_id == "plan_b"


def test_explain_selection_returns_evaluation() -> None:
    identity = make_test_identity()
    _, plan_b = make_test_plans()

    controller = IdentityController(identity)
    ev = controller.explain_selection(plan_b)

    assert ev.plan_id == "plan_b"
    assert isinstance(ev.total_score, float)


if __name__ == "__main__":
    test_value_evaluation_returns_scores()
    test_identity_controller_evaluates_multiple_plans()
    test_value_aligned_selection_prefers_safer_plan()
    test_explain_selection_returns_evaluation()
    print("All A10 identity/value tests passed.")
