"""A7 rule engine for evaluating constraints."""

from __future__ import annotations

from typing import List

from .types import Constraint, ConstraintResult, DecisionProposal, WorldState


class RuleEngine:
    """Small deterministic engine for evaluating registered constraints."""

    def __init__(self) -> None:
        self.constraints: List[Constraint] = []

    def add(self, constraint: Constraint) -> None:
        """Register a constraint."""
        self.constraints.append(constraint)

    def evaluate_all(self, proposal: DecisionProposal, world: WorldState) -> List[ConstraintResult]:
        """Evaluate all constraints that apply to the proposal."""
        results: List[ConstraintResult] = []

        for constraint in self.constraints:
            if proposal.decision_type not in constraint.applies_to:
                continue

            if constraint.required_tags and not constraint.required_tags.intersection(proposal.tags):
                continue

            try:
                ok = bool(constraint.predicate(proposal, world))
                message = "ok" if ok else constraint.description
            except Exception as exc:  # defensive: failed rules should fail closed
                ok = False
                message = f"constraint evaluation error: {exc}"

            results.append(
                ConstraintResult(
                    constraint_id=constraint.constraint_id,
                    ok=ok,
                    severity=constraint.severity,
                    message=message,
                )
            )

        return results
