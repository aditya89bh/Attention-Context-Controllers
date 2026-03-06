"""A10 evaluator.

A deterministic evaluator that scores a candidate response against A10 constraints.

This is deliberately simple: keyword/regex-like heuristics can be layered later.
"""

from __future__ import annotations

from .types import DriftSignal, EvaluationResult, PolicyConstraint


class Evaluator:
    """Evaluate text against constraints and emit drift signals."""

    def evaluate(self, text: str, constraints: list[PolicyConstraint]) -> EvaluationResult:
        """Return an EvaluationResult indicating if the text violates constraints."""
        signals: list[DriftSignal] = []
        drift = 0.0

        lowered = text.lower()
        for c in constraints:
            # Minimal heuristic: if a constraint contains "do not X", flag if X appears.
            # This is not meant to be smart; it is a scaffold for future rules.
            key = c.text.lower().replace("do not ", "").strip()
            if key and key in lowered:
                sev = 2.0 if c.severity == "hard" else 1.0
                drift += sev
                signals.append(
                    DriftSignal(
                        signal_id=f"constraint_hit:{c.constraint_id}",
                        description=f"Potential violation of constraint: {c.text}",
                        score=sev,
                        meta={"matched": key},
                    )
                )

        ok = drift == 0.0
        return EvaluationResult(ok=ok, drift_score=drift, signals=signals)
