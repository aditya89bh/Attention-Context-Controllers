"""A10 Identity & Value Stabilization controller.

Biases plan selection using deterministic, rule-based value evaluation.
"""

from __future__ import annotations

from typing import List

from a10.types import IdentityProfile, ValueConfig, ValueEvaluation
from a10.values import ValueEvaluator
from a9.types import Plan


class IdentityController:
    """Bias plan selection using an agent's identity and value weights."""

    def __init__(self, identity: IdentityProfile, config: ValueConfig | None = None) -> None:
        self.identity = identity
        self.config = config or ValueConfig()
        self.evaluator = ValueEvaluator(identity, self.config)

    def evaluate_plans(self, plans: List[Plan]) -> List[ValueEvaluation]:
        """Evaluates candidate plans using the agent’s value system."""
        evaluations: List[ValueEvaluation] = []
        for p in plans:
            evaluations.append(self.evaluator.evaluate_plan(p))
        return evaluations

    def select_value_aligned_plan(self, plans: List[Plan]) -> Plan | None:
        """Selects the plan most aligned with the agent’s identity and value weights."""
        if not plans:
            return None

        evals = self.evaluate_plans(plans)
        best_idx = 0
        best_score = evals[0].total_score
        for i, e in enumerate(evals[1:], start=1):
            if e.total_score > best_score:
                best_idx = i
                best_score = e.total_score
        return plans[best_idx]

    def explain_selection(self, plan: Plan) -> ValueEvaluation:
        """Returns the value-based evaluation explaining why a plan aligns with identity preferences."""
        return self.evaluator.evaluate_plan(plan)
