"""
A7 — Constraint Enforcement Controller

This module implements the enforcement layer of A7.

A6 chooses what the agent wants to do.
A7 validates whether it is allowed and coherent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .types import (
    Commitment,
    Constraint,
    ConstraintResult,
    DecisionProposal,
    EnforcementMode,
    ValidationReport,
    WorldState,
)
from .rules import RuleEngine


@dataclass
class PenaltyPolicy:
    """
    Numeric penalties used to communicate violation severity upstream.
    """

    soft_violation_penalty: float = 2.0
    hard_violation_penalty: float = 10.0


class ConsistencyController:
    """
    A7 enforcement layer.

    Responsibilities:
    - register constraints
    - validate decision proposals against constraints
    - enforce HARD vs SOFT violations under an EnforcementMode
    - manage commitments
    - record accepted or blocked decisions into world history
    """

    def __init__(
        self,
        mode: EnforcementMode = EnforcementMode.STRICT,
        penalty_policy: Optional[PenaltyPolicy] = None,
    ):
        self.mode = mode
        self.penalty_policy = penalty_policy or PenaltyPolicy()
        self.engine = RuleEngine()

    def add_constraint(self, constraint: Constraint) -> None:
        """Register a constraint."""
        self.engine.add(constraint)

    def commit(self, world: WorldState, commitment: Commitment) -> None:
        """Add an active commitment into world state."""
        world.add_commitment(commitment)
        world.record({"type": "commitment_added", "commitment": commitment.commitment_id})

    def retract_commitment(self, world: WorldState, commitment_id: str) -> None:
        """Deactivate a commitment without deleting it."""
        if commitment_id in world.commitments:
            world.commitments[commitment_id].active = False
            world.record({"type": "commitment_retracted", "commitment": commitment_id})

    def validate(self, proposal: DecisionProposal, world: WorldState) -> ValidationReport:
        """Validate a proposal against all constraints and return a structured report."""
        results = self.engine.evaluate_all(proposal, world)
        allowed, penalties = self._enforce(results)

        notes: Dict[str, Any] = {
            "history_len": len(world.history),
            "active_commitments": [cid for cid, c in world.commitments.items() if c.active],
        }

        return ValidationReport(
            proposal=proposal,
            allowed=allowed,
            mode=self.mode,
            results=results,
            penalties=penalties,
            notes=notes,
        )

    def apply_if_allowed(self, report: ValidationReport, world: WorldState) -> bool:
        """
        Log accepted or blocked proposals.
        """
        if not report.allowed:
            world.record(
                {
                    "type": "proposal_blocked",
                    "proposal": report.proposal.decision_id,
                    "payload": report.proposal.payload,
                    "results": [r.__dict__ for r in report.results],
                    "penalties": report.penalties,
                }
            )
            return False

        world.record(
            {
                "type": "proposal_accepted",
                "proposal": report.proposal.decision_id,
                "payload": report.proposal.payload,
                "penalties": report.penalties,
            }
        )
        return True

    def _enforce(self, results: List[ConstraintResult]) -> Tuple[bool, Dict[str, float]]:
        """
        Convert constraint results into an allowed boolean and penalties mapping.
        """
        penalties: Dict[str, float] = {}

        hard = [r for r in results if (not r.ok and r.severity == "HARD")]
        soft = [r for r in results if (not r.ok and r.severity == "SOFT")]

        if hard:
            for r in hard:
                penalties[r.constraint_id] = self.penalty_policy.hard_violation_penalty
            if self.mode == EnforcementMode.STRICT:
                return False, penalties
            return True, penalties

        if soft:
            for r in soft:
                penalties[r.constraint_id] = self.penalty_policy.soft_violation_penalty
            return True, penalties

        return True, penalties
