"""A10 deterministic value evaluation logic."""

from __future__ import annotations

from typing import Any, List

from .types import IdentityProfile, ValueCategory, ValueConfig, ValueEvaluation, ValueScore


class ValueEvaluator:
    """Deterministic plan evaluator based on identity value weights."""

    def __init__(self, identity: IdentityProfile, config: ValueConfig | None = None) -> None:
        self.identity = identity
        self.config = config or ValueConfig()

    def evaluate_plan(self, plan: Any) -> ValueEvaluation:
        """Evaluate a plan against the identity's value weights."""
        steps = getattr(plan, "steps", [])
        step_count = len(steps)

        total_risk = sum(float(step.action.risk) for step in steps)
        total_cost = sum(float(step.action.cost) for step in steps)
        action_names = [step.action.name for step in steps]

        raw = {
            ValueCategory.SAFETY: -total_risk,
            ValueCategory.EFFICIENCY: -float(step_count),
            ValueCategory.ACCURACY: 2.0 if any(name in ("verify", "revise") for name in action_names) else 0.0,
            ValueCategory.TRANSPARENCY: 1.0 if any(name in ("outline", "plan") for name in action_names) else 0.0,
            ValueCategory.RESOURCE_USE: -total_cost,
        }

        scores: List[ValueScore] = []
        weighted_total = 0.0
        bias = float(self.config.bias_strength)

        for category in ValueCategory:
            weight = float(self.identity.value_weights.get(category, 0.0))
            weighted = raw[category] * weight * bias
            weighted_total += weighted
            reason = f"raw={raw[category]:.3f} * weight={weight:.3f} * bias_strength={bias:.3f}"
            scores.append(ValueScore(category=category, score=float(weighted), reason=reason))

        norm = float(self.config.normalization_factor) or 1.0
        total_score = float(weighted_total / norm)

        return ValueEvaluation(
            plan_id=getattr(plan, "plan_id", "unknown_plan"),
            scores=scores,
            total_score=total_score,
            notes={
                "step_count": str(step_count),
                "bias_strength": str(bias),
            },
        )
