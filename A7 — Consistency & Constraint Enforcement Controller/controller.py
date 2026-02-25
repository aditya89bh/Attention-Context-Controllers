"""
A7 — Consistency & Constraint Enforcement Controller (controller.py)

This module implements the enforcement layer of A7.

It is intentionally kept free of domain rules.
All built-in constraint constructors live in constraints.py.

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

    Typical usage:
      - A6 subtracts penalties from candidate goal/action scores.
      - A8 monitors repeated violations or repeated penalties over time.
    """
    soft_violation_penalty: float = 2.0
    hard_violation_penalty: float = 10.0


class ConsistencyController:
    """
    A7 enforcement layer.

    Responsibilities:
      - Register constraints (predicate rules)
      - Validate DecisionProposals against constraints
      - Enforce HARD vs SOFT violations under an EnforcementMode
      - Manage commitments (promises/locks)
      - Record accepted/blocked decisions into world history (optional)

    Non-responsibilities:
      - No execution
      - No planning
      - No learning
      - No LLM internals
    """

    def __init__(
        self,
        mode: EnforcementMode = EnforcementMode.STRICT,
        penalty_policy: Optional[PenaltyPolicy] = None,
    ):
        self.mode = mode
        self.penalty_policy = penalty_policy or PenaltyPolicy()
        self.engine = RuleEngine()

    # -----------------------
    # Constraint registration
    # -----------------------
    def add_constraint(self, constraint: Constraint) -> None:
        """Register a constraint (invariant/policy)."""
        self.engine.add(constraint)

    # -----------------------
    # Commitment management
    # -----------------------
    def commit(self, world: WorldState, commitment: Commitment) -> None:
        """Add an active commitment into world state."""
        world.add_commitment(commitment)
        world.record({"type": "commitment_added", "commitment": commitment.commitment_id})

    def retract_commitment(self, world: WorldState, commitment_id: str) -> None:
        """Deactivate a commitment without deleting it."""
        if commitment_id in world.commitments:
            world.commitments[commitment_id].active = False
            world.record({"type": "commitment_retracted", "commitment": commitment_id})

    # -----------------------
    # Validation
    # -----------------------
    def validate(self, proposal: DecisionProposal, world: WorldState) -> ValidationReport:
        """
        Validate a proposal against all constraints and return a structured report.
        """
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
        Convenience logger:
          - If blocked: record proposal_blocked with reasons.
          - If allowed: record proposal_accepted.

        Returns True if accepted, False if blocked.
        """
        if not report.allowed:
            world.record({
                "type": "proposal_blocked",
                "proposal": report.proposal.decision_id,
                "payload": report.proposal.payload,
                "results": [r.__dict__ for r in report.results],
                "penalties": report.penalties,
            })
            return False

        world.record({
            "type": "proposal_accepted",
            "proposal": report.proposal.decision_id,
            "payload": report.proposal.payload,
            "penalties": report.penalties,
        })
        return True

    # -----------------------
    # Enforcement policy
    # -----------------------
    def _enforce(self, results: List[ConstraintResult]) -> Tuple[bool, Dict[str, float]]:
        """
        Convert constraint results into:
          - allowed boolean
          - penalties mapping

        Rules:
          - HARD violations:
              STRICT -> block
              SOFT/AUDIT -> allow but penalize
          - SOFT violations:
              allow but penalize
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
