"""A9 deterministic long-horizon planner.

This module provides:
- deterministic candidate plan generation (beam search)
- deterministic plan selection using the PlanSimulator
- commitment tracking with abandonment + replanning triggers

No randomness, no external calls.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Optional

from .types import (
    Action,
    Goal,
    Plan,
    PlanStatus,
    PlanStep,
    PlannerConfig,
)
from .simulator import PlanSimulator


class LongHorizonPlanner:
    """Deterministic candidate plan generation + commitment controller."""

    def __init__(self, config: PlannerConfig | None = None):
        """Create the planner with a config and an internal deterministic simulator."""
        self.config = config or PlannerConfig()
        self.simulator = PlanSimulator()
        self.active_plan: Plan | None = None

    def generate_candidate_plans(self, goal: Goal) -> list[Plan]:
        """Generate candidate plans deterministically using beam search.

        Behavior:
        - pick an action library based on goal.tags
        - beam search expands plans by appending actions in a fixed order
        - keep top `beam_width` partial plans by simulated score
        - return final beam (size <= beam_width)
        """

        tags = set(t.lower() for t in goal.tags)
        if "writing" in tags:
            action_names = ["outline", "draft", "revise", "publish"]
        else:
            action_names = ["analyze", "plan", "execute", "verify"]

        # fixed library: same cost/risk defaults (caller can adjust later)
        library = [Action(name=n) for n in action_names]

        max_depth = int(self.config.max_plan_depth)
        beam_width = int(self.config.beam_width)

        # Beam holds partial step sequences (list[PlanStep])
        beam: list[list[PlanStep]] = [[]]

        for depth in range(max_depth):
            expanded: list[list[PlanStep]] = []
            for partial_steps in beam:
                for a in library:
                    steps = list(partial_steps)
                    step_id = f"s{len(steps)}"
                    steps.append(
                        PlanStep(
                            step_id=step_id,
                            action=a,
                            expected_outcome=f"Complete {a.name}",
                        )
                    )
                    expanded.append(steps)

            # Score partial plans deterministically with the simulator
            scored: list[tuple[float, list[PlanStep]]] = []
            for steps in expanded:
                plan = Plan(
                    plan_id="_partial",
                    goal_id=goal.goal_id,
                    steps=steps,
                    status=PlanStatus.DRAFT,
                )
                sim = self.simulator.simulate(plan)
                scored.append((sim.score, steps))

            # Keep top beam_width (highest score), deterministic tie-breaker by step names
            scored.sort(key=lambda x: (x[0], [s.action.name for s in x[1]]), reverse=True)
            beam = [steps for _, steps in scored[:beam_width]]

        # Convert final beam into Plans with deterministic plan_ids
        plans: list[Plan] = []
        for i, steps in enumerate(beam):
            plans.append(
                Plan(
                    plan_id=f"plan_{i}",
                    goal_id=goal.goal_id,
                    steps=list(steps),
                    status=PlanStatus.DRAFT,
                )
            )
        return plans

    def select_best_plan(self, plans: list[Plan]) -> Plan:
        """Select the plan with the highest simulated score.

        Raises:
            ValueError: if plans is empty.
        """
        if not plans:
            raise ValueError("select_best_plan() received empty plans list")

        best = None
        best_score = None
        for p in plans:
            r = self.simulator.simulate(p)
            if best is None or r.score > best_score:  # type: ignore[operator]
                best = p
                best_score = r.score
        assert best is not None
        return best

    def commit(self, plan: Plan) -> Plan:
        """Activate a plan and set commitment to maximum."""
        plan.status = PlanStatus.ACTIVE
        plan.commitment_strength = 1.0
        self.active_plan = plan
        return plan

    def tick_after_step(self, success: bool) -> None:
        """Update commitment after attempting one step.

        - On failure, decay commitment.
        - On success, recover a bit (capped at 1.0).
        - If commitment falls below abandonment threshold, abandon the plan.
        """
        if self.active_plan is None:
            return

        decay = float(self.config.commitment_decay)
        if not success:
            self.active_plan.commitment_strength -= decay
        else:
            self.active_plan.commitment_strength = min(
                1.0, self.active_plan.commitment_strength + (decay / 2.0)
            )

        if self.active_plan.commitment_strength < float(self.config.abandonment_threshold):
            self.active_plan.status = PlanStatus.ABANDONED
            self.active_plan = None

    def next_step(self) -> PlanStep | None:
        """Return the next step to execute without advancing the plan."""
        if self.active_plan is None:
            return None

        if self.active_plan.current_step_index >= len(self.active_plan.steps):
            self.active_plan.status = PlanStatus.COMPLETED
            self.active_plan = None
            return None

        return self.active_plan.steps[self.active_plan.current_step_index]

    def advance_step(self) -> None:
        """Advance to the next step of the active plan (if any)."""
        if self.active_plan is None:
            return
        self.active_plan.current_step_index += 1
