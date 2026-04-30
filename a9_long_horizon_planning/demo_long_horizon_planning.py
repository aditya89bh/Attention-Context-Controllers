"""A9 Long-Horizon Planning Demo.

Run:
    python a9_long_horizon_planning/demo_long_horizon_planning.py

This demo shows candidate plan generation, plan selection, commitment, and abandonment risk.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from a9_long_horizon_planning.a9 import Goal, LongHorizonPlanner, PlannerConfig  # noqa: E402


def main() -> None:
    goal = Goal(
        goal_id="recover_failed_pickup_safely",
        description="Recover failed pickup safely during CNC loading",
        priority=1.0,
        tags=["robotics"],
    )

    planner = LongHorizonPlanner(
        PlannerConfig(
            max_plan_depth=4,
            beam_width=3,
            commitment_decay=0.25,
            abandonment_threshold=0.35,
        )
    )

    plans = planner.generate_candidate_plans(goal)
    best_plan = planner.select_best_plan(plans)
    planner.commit(best_plan)

    print("=== A9 Long-Horizon Planning Demo ===")
    print("\nSelected Goal:")
    print(f"- {goal.goal_id}: {goal.description}")

    print("\nCandidate Plans:")
    for plan in plans:
        actions = " -> ".join(step.action.name for step in plan.steps)
        score = planner.simulator.simulate(plan).score
        print(f"- {plan.plan_id}: {actions} | score={score:.2f}")

    print("\nCommitted Plan:")
    print(f"- {best_plan.plan_id}")
    print("- " + " -> ".join(step.action.name for step in best_plan.steps))
    print(f"- commitment_strength={best_plan.commitment_strength:.2f}")

    print("\nExecution Trace:")
    outcomes = [True, False, False, True]
    for outcome in outcomes:
        step = planner.next_step()
        if step is None:
            break
        print(f"Step: {step.action.name} | success={outcome}")
        planner.tick_after_step(success=outcome)
        if planner.active_plan is None:
            print("Plan abandoned due to low commitment. Replanning should trigger.")
            break
        print(f"Commitment after step: {planner.active_plan.commitment_strength:.2f}")
        if outcome:
            planner.advance_step()

    print("\nTakeaway:")
    print("Long-horizon planning helps the agent commit to a sequence while still allowing abandonment when progress collapses.")


if __name__ == "__main__":
    main()
