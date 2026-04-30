"""Smoke tests for normalized controller modules.

Run from repo root:
    python -m pytest tests/test_smoke.py
"""

from __future__ import annotations


def test_a7_imports() -> None:
    from a7_constraint_enforcement import ConsistencyController, DecisionProposal, DecisionType, WorldState

    controller = ConsistencyController()
    proposal = DecisionProposal(
        decision_id="p1",
        decision_type=DecisionType.ACTION,
        payload={"action": "inspect"},
        tags=set(),
    )
    report = controller.validate(proposal, WorldState())
    assert report.allowed is True


def test_a8_imports() -> None:
    from a8_self_monitoring.controller import SelfMonitoringController

    controller = SelfMonitoringController()
    report = controller.analyze([])
    assert report.issues == []


def test_a9_imports() -> None:
    from a9_long_horizon_planning.a9 import Goal, LongHorizonPlanner

    planner = LongHorizonPlanner()
    plans = planner.generate_candidate_plans(Goal(goal_id="g1", description="test goal"))
    assert len(plans) > 0


def test_a10_imports() -> None:
    from a10_identity_value_stabilization.a10 import IdentityProfile, ValueCategory, IdentityController
    from a9_long_horizon_planning.a9 import Action, Plan, PlanStatus, PlanStep

    identity = IdentityProfile(
        agent_id="test_agent",
        description="Test agent",
        value_weights={ValueCategory.SAFETY: 1.0},
        created_at="2026-04-30",
    )
    plan = Plan(
        plan_id="p1",
        goal_id="g1",
        steps=[
            PlanStep(
                step_id="s1",
                action=Action(name="verify", risk=0.1, cost=1.0),
                expected_outcome="verified",
            )
        ],
        status=PlanStatus.DRAFT,
    )
    controller = IdentityController(identity)
    selected = controller.select_value_aligned_plan([plan])
    assert selected == plan
