"""A10 deterministic value evaluation logic.

This module implements transparent, fully rule-based scoring of candidate plans
against an agent's value weights.

No randomness. No ML.
"""

from __future__ import annotations

from typing import List

from a10.types import (
    IdentityProfile,
    ValueCategory,
    ValueConfig,
    ValueEvaluation,
    ValueScore,
)
from a9.types import Plan


class ValueEvaluator:
    """Deterministic plan evaluator based on identity value weights."""

    def __init__(self, identity: IdentityProfile, config: ValueConfig | None = None) -> None:
        self.identity = identity
        self.config = config or ValueConfig()

    def evaluate_plan(self, plan: Plan) -> ValueEvaluation:
        """Evaluate a plan against the identity's value weights.

        The evaluation is deterministic and based on simple plan properties
        (step count, action names, summed cost, summed risk).
        """

        steps = plan.steps
        step_count = len(steps)

        total_risk = sum(float(s.action.risk) for s in steps)
        total_cost = sum(float(s.action.cost) for s in steps)
        action_names = [s.action.name for s in steps]

        # Raw scores per category (rule-based)
        raw = {
            ValueCategory.SAFETY: -total_risk,
            ValueCategory.EFFICIENCY: -float(step_count),
            ValueCategory.ACCURACY: 2.0 if any(n in ("verify", "revise") for n in action_names) else 0.0,
            ValueCategory.TRANSPARENCY: 1.0 if any(n in ("outline", "plan") for n in action_names) else 0.0,
            ValueCategory.RESOURCE_USE: -total_cost,
        }

        scores: List[ValueScore] = []
        weighted_total = 0.0
        bias = float(self.config.bias_strength)

        for cat in ValueCategory:
            weight = float(self.identity.value_weights.get(cat, 0.0))
            weighted = raw[cat] * weight * bias
            weighted_total += weighted

            reason = (
                f"raw={raw[cat]:.3f} * weight={weight:.3f} * bias_strength={bias:.3f}"
            )
            scores.append(ValueScore(category=cat, score=float(weighted), reason=reason))

        norm = float(self.config.normalization_factor) or 1.0
        total_score = float(weighted_total / norm)

        return ValueEvaluation(
            plan_id=plan.plan_id,
            scores=scores,
            total_score=total_score,
            notes={
                "step_count": str(step_count),
                "bias_strength": str(bias),
            },
        )
