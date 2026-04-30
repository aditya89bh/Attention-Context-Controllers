"""A10 Identity and Value Stabilization controller."""

from __future__ import annotations

from typing import Any, List

from .types import IdentityProfile, ValueConfig, ValueEvaluation
from .values import ValueEvaluator


class IdentityController:
    """Bias plan selection using an agent's identity and value weights."""

    def __init__(self, identity: IdentityProfile, config: ValueConfig | None = None) -> None:
        self.identity = identity
        self.config = config or ValueConfig()
        self.evaluator = ValueEvaluator(identity, self.config)

    def evaluate_plans(self, plans: List[Any]) -> List[ValueEvaluation]:
        """Evaluate candidate plans using the agent's value system."""
        return [self.evaluator.evaluate_plan(plan) for plan in plans]

    def select_value_aligned_plan(self, plans: List[Any]) -> Any | None:
        """Select the plan most aligned with the agent's identity and value weights."""
        if not plans:
            return None

        evaluations = self.evaluate_plans(plans)
        best_index = 0
        best_score = evaluations[0].total_score

        for index, evaluation in enumerate(evaluations[1:], start=1):
            if evaluation.total_score > best_score:
                best_index = index
                best_score = evaluation.total_score

        return plans[best_index]

    def explain_selection(self, plan: Any) -> ValueEvaluation:
        """Return the value-based evaluation explaining why a plan aligns with values."""
        return self.evaluator.evaluate_plan(plan)
