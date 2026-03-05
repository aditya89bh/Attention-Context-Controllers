"""A9 deterministic plan simulator.

This is a toy, deterministic simulator used to score candidate plans.
It intentionally includes **no ML**, **no stochasticity**, and no external
dependencies.
"""

from __future__ import annotations

from .types import Action, Plan, PlanStep, SimResult


class PlanSimulator:
    """Toy deterministic simulator for scoring plans."""

    def __init__(self) -> None:
        # Scoring constants
        self.step_cost_penalty = -1.0
        self.risk_penalty_factor = -2.0
        self.goal_reward = 20.0

    def simulate(self, plan: Plan) -> SimResult:
        """Simulate (score) a plan deterministically and return a SimResult."""

        num_steps = len(plan.steps)
        if num_steps == 0:
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
            + (self.step_cost_penalty * num_steps)
            + (self.risk_penalty_factor * risk_score)
        )

        return SimResult(
            plan_id=plan.plan_id,
            score=float(score),
            total_cost=float(total_cost),
            risk_score=float(risk_score),
            success=True,
            notes={"number_of_steps": num_steps},
        )
