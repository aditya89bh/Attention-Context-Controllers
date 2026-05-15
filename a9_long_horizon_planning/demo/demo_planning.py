"""End-to-end demo for A9 — Long-Horizon Planning & Commitment Controller.

Run from repo root:
  python3 A9_long_horizon_planning/demo/demo_planning.py

This demo is deterministic and intentionally simple.
"""

from __future__ import annotations

from a9.types import Goal, PlannerConfig
from a9.goal_tree import GoalTree
from a9.planner import LongHorizonPlanner


def main() -> None:
    # 1) Root goal
    goal = Goal(
        goal_id="publish_a9",
        description="Publish A9 planning module",
        priority=1.0,
        tags=["writing"],
    )

    # 2) Build GoalTree
    tree = GoalTree(goal)
    tree.add_subgoal(
        "publish_a9",
        Goal(goal_id="write_code", description="Write code files", priority=1.0),
    )
    tree.add_subgoal(
        "publish_a9",
        Goal(goal_id="add_demo", description="Add demo", priority=1.0),
    )
    tree.add_subgoal(
        "publish_a9",
        Goal(goal_id="push_repo", description="Push to GitHub", priority=1.0),
    )

    # 3) Print the goal tree
    print("\nGOAL TREE")
    tree.print_tree()

    # 4) Initialize planner
    planner = LongHorizonPlanner(PlannerConfig(max_plan_depth=4, beam_width=3))

    # 5) Generate candidate plans
    plans = planner.generate_candidate_plans(goal)

    # 6) Print all generated plans
    print("\nCANDIDATE PLANS")
    for p in plans:
        actions = [s.action.name for s in p.steps]
        print(f"- {p.plan_id}: {actions}")

    # 7) Select best plan
    best_plan = planner.select_best_plan(plans)
    print("\nSELECTED PLAN")
    print(f"Selected: {best_plan.plan_id}")

    # 8) Commit plan
    planner.commit(best_plan)

    # 9) Deterministic execution loop (all steps succeed)
    print("\nEXECUTION")
    while True:
        step = planner.next_step()
        if step is None:
            break
        print(f"Executing {step.step_id}: {step.action.name}")
        planner.tick_after_step(success=True)
        planner.advance_step()

    # 10) Print final status
    print("\nFINAL STATUS")
    print(best_plan.status)


if __name__ == "__main__":
    main()
