"""A9 deterministic long-horizon planner."""

from __future__ import annotations

from .simulator import PlanSimulator
from .types import Action, Goal, Plan, PlannerConfig, PlanStatus, PlanStep


class LongHorizonPlanner:
    """Deterministic candidate plan generation plus commitment controller."""

    def __init__(self, config: PlannerConfig | None = None):
        self.config = config or PlannerConfig()
        self.simulator = PlanSimulator()
        self.active_plan: Plan | None = None

    def generate_candidate_plans(self, goal: Goal) -> list[Plan]:
        """Generate candidate plans deterministically using beam search."""
        tags = set(tag.lower() for tag in goal.tags)
        if "writing" in tags:
            action_names = ["outline", "draft", "revise", "publish"]
        elif "robotics" in tags:
            action_names = ["inspect", "adjust", "retry", "verify"]
        else:
            action_names = ["analyze", "plan", "execute", "verify"]

        library = [Action(name=name) for name in action_names]
        beam: list[list[PlanStep]] = [[]]

        for _ in range(int(self.config.max_plan_depth)):
            expanded: list[list[PlanStep]] = []
            for partial_steps in beam:
                for action in library:
                    steps = list(partial_steps)
                    step_id = f"s{len(steps)}"
                    steps.append(
                        PlanStep(
                            step_id=step_id,
                            action=action,
                            expected_outcome=f"Complete {action.name}",
                        )
                    )
                    expanded.append(steps)

            scored: list[tuple[float, list[PlanStep]]] = []
            for steps in expanded:
                plan = Plan(
                    plan_id="_partial",
                    goal_id=goal.goal_id,
                    steps=steps,
                    status=PlanStatus.DRAFT,
                )
                result = self.simulator.simulate(plan)
                scored.append((result.score, steps))

            scored.sort(key=lambda item: (item[0], [step.action.name for step in item[1]]), reverse=True)
            beam = [steps for _, steps in scored[: int(self.config.beam_width)]]

        plans: list[Plan] = []
        for index, steps in enumerate(beam):
            plans.append(
                Plan(
                    plan_id=f"plan_{index}",
                    goal_id=goal.goal_id,
                    steps=list(steps),
                    status=PlanStatus.DRAFT,
                )
            )
        return plans

    def select_best_plan(self, plans: list[Plan]) -> Plan:
        """Select the plan with the highest simulated score."""
        if not plans:
            raise ValueError("select_best_plan() received an empty plans list")

        best_plan = plans[0]
        best_score = self.simulator.simulate(best_plan).score

        for plan in plans[1:]:
            score = self.simulator.simulate(plan).score
            if score > best_score:
                best_plan = plan
                best_score = score

        return best_plan

    def commit(self, plan: Plan) -> Plan:
        """Activate a plan and set commitment to maximum."""
        plan.status = PlanStatus.ACTIVE
        plan.commitment_strength = 1.0
        self.active_plan = plan
        return plan

    def tick_after_step(self, success: bool) -> None:
        """Update commitment after one attempted step."""
        if self.active_plan is None:
            return

        decay = float(self.config.commitment_decay)
        if success:
            self.active_plan.commitment_strength = min(
                1.0,
                self.active_plan.commitment_strength + (decay / 2.0),
            )
        else:
            self.active_plan.commitment_strength -= decay

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
        """Advance to the next step of the active plan."""
        if self.active_plan is None:
            return
        self.active_plan.current_step_index += 1
