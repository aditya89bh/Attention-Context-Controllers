"""Demo: A9 long-horizon planning & commitment controller.

Run from repo root:
  python3 A9_long_horizon_planning/demo/demo_planning.py

This demo intentionally uses a deterministic, toy setup:
- a root goal decomposed into subgoals (GoalTree)
- deterministic candidate plan generation (beam search)
- deterministic plan scoring (PlanSimulator)
- commitment decay on repeated failures with abandonment
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running this script directly from the repo root.
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from A9_long_horizon_planning.a9.goal_tree import GoalTree
from A9_long_horizon_planning.a9.planner import LongHorizonPlanner
from A9_long_horizon_planning.a9.types import Goal, PlannerConfig


def main() -> None:
    # ---- Goal decomposition ----
    root = Goal(goal_id="g_root", description="Publish A9 Repo", tags=["writing"], priority=1.0)
    tree = GoalTree(root)

    tree.add_subgoal("g_root", Goal(goal_id="g_code", description="Write Code Files"))
    tree.add_subgoal("g_root", Goal(goal_id="g_demo", description="Add Demo"))
    tree.add_subgoal("g_root", Goal(goal_id="g_push", description="Push to GitHub"))

    print("\nGoal tree:")
    tree.print_tree()

    print("\nOpen goals (leaves-first):")
    for n in tree.get_open_goals():
        print(f"- {n.goal.goal_id}: {n.goal.description}")

    # ---- Planning ----
    config = PlannerConfig(max_plan_depth=4, beam_width=3)
    planner = LongHorizonPlanner(config=config)

    candidates = planner.generate_candidate_plans(root)
    best = planner.select_best_plan(candidates)
    planner.commit(best)

    print("\nSelected plan:")
    for i, step in enumerate(best.steps):
        print(f"  {i}. {step.action.name} (cost={step.action.cost}, risk={step.action.risk})")

    # ---- Commitment demo ----
    # Simulate execution: fail twice, then succeed.
    print("\nCommitment over steps (simulate failures):")
    for attempt in range(6):
        step = planner.next_step()
        if step is None:
            print("Plan finished or abandoned.")
            break

        success = not (attempt in (1, 2))  # deterministic failures
        print(
            f"Attempt {attempt}: step={step.step_id}:{step.action.name} success={success} "
            f"commitment={planner.active_plan.commitment_strength if planner.active_plan else None}"
        )

        planner.tick_after_step(success=success)
        if planner.active_plan is None:
            print("Plan abandoned due to low commitment → replanning would trigger here.")
            break

        # Advance only on success
        if success:
            planner.advance_step()


if __name__ == "__main__":
    main()
