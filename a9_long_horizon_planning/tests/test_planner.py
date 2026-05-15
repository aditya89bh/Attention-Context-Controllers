"""Deterministic sanity tests for A9 planning modules.

- No external test frameworks.
- Plain Python assertions.

Run:
  python3 A9_long_horizon_planning/tests/test_planner.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure `a9/` is importable when running directly.
ROOT = Path(__file__).resolve().parents[2]
A9_ROOT = ROOT / "A9_long_horizon_planning"
if str(A9_ROOT) not in sys.path:
    sys.path.insert(0, str(A9_ROOT))

from a9.types import Goal, PlannerConfig, PlanStatus
from a9.goal_tree import GoalTree
from a9.planner import LongHorizonPlanner


def test_goal_tree_creation() -> None:
    root = Goal(goal_id="root", description="Root goal")
    tree = GoalTree(root)
    tree.add_subgoal("root", Goal(goal_id="s1", description="Subgoal 1"))
    tree.add_subgoal("root", Goal(goal_id="s2", description="Subgoal 2"))

    assert tree.root is not None
    assert tree.root.goal.goal_id == "root"
    assert len(tree.root.children) == 2


def test_plan_generation() -> None:
    goal = Goal(goal_id="g", description="Write something", tags=["writing"])
    cfg = PlannerConfig(max_plan_depth=4, beam_width=3)
    planner = LongHorizonPlanner(cfg)

    plans = planner.generate_candidate_plans(goal)
    assert len(plans) > 0
    for p in plans:
        assert len(p.steps) > 0
        assert len(p.steps) <= cfg.max_plan_depth


def test_plan_selection() -> None:
    goal = Goal(goal_id="g", description="Write something", tags=["writing"])
    cfg = PlannerConfig(max_plan_depth=4, beam_width=3)
    planner = LongHorizonPlanner(cfg)

    plans = planner.generate_candidate_plans(goal)
    best = planner.select_best_plan(plans)
    assert best is not None


def test_commitment_and_execution() -> None:
    goal = Goal(goal_id="g", description="Write something", tags=["writing"])
    cfg = PlannerConfig(max_plan_depth=4, beam_width=3)
    planner = LongHorizonPlanner(cfg)

    plans = planner.generate_candidate_plans(goal)
    best = planner.select_best_plan(plans)
    planner.commit(best)

    while True:
        step = planner.next_step()
        if step is None:
            break
        planner.tick_after_step(success=True)
        planner.advance_step()

    assert best.status == PlanStatus.COMPLETED


if __name__ == "__main__":
    test_goal_tree_creation()
    test_plan_generation()
    test_plan_selection()
    test_commitment_and_execution()
    print("All A9 planner tests passed.")
