"""A9 deterministic plan simulator."""

from __future__ import annotations

from .types import Plan, SimResult


class PlanSimulator:
    """Toy deterministic simulator for scoring plans."""

    def __init__(self) -> None:
        self.step_cost_penalty = -1.0
        self.risk_penalty_factor = -2.0
        self.goal_reward = 20.0

    def simulate(self, plan: Plan) -> SimResult:
        """Simulate and score a plan deterministically."""
        number_of_steps = len(plan.steps)
        if number_of_steps == 0:
            return SimResult(
                plan_id=plan.plan_id,
                score=-10.0,
                total_cost=0.0,
                risk_score=0.0,
                success=False,
                notes={"number_of_steps": 0},
            )

        total_cost = 0.0
        risk_score = 0.0
        for step in plan.steps:
            total_cost += float(step.action.cost)
            risk_score += float(step.action.risk)

        score = (
            self.goal_reward
            + (self.step_cost_penalty * number_of_steps)
            + (self.risk_penalty_factor * risk_score)
        )

        return SimResult(
            plan_id=plan.plan_id,
            score=float(score),
            total_cost=float(total_cost),
            risk_score=float(risk_score),
            success=True,
            notes={"number_of_steps": number_of_steps},
        )
