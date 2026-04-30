"""
A7 — Built-in Constraints Library

This module contains reusable constraint constructors that plug into the
A7 ConsistencyController.
"""

from __future__ import annotations

from .types import Constraint, DecisionProposal, DecisionType, WorldState


def constraint_require_human_for_irreversible() -> Constraint:
    """
    Safety gate: if a proposal is tagged irreversible, require explicit approval.
    """

    def pred(proposal: DecisionProposal, world: WorldState) -> bool:
        if "irreversible" not in proposal.tags:
            return True
        return bool(world.facts.get("human_approved", False))

    return Constraint(
        constraint_id="require_human_for_irreversible",
        name="Human approval for irreversible actions",
        description="Blocked: irreversible action requires world.facts['human_approved']=True.",
        severity="HARD",
        applies_to={DecisionType.ACTION},
        predicate=pred,
        required_tags={"irreversible"},
    )


def constraint_no_contradict_commitment(commitment_tag: str = "no_send_email") -> Constraint:
    """
    Commitment coherence gate.

    Blocks an ACTION proposal that contradicts an active commitment tag.
    """

    def pred(proposal: DecisionProposal, world: WorldState) -> bool:
        if proposal.decision_type != DecisionType.ACTION:
            return True

        if proposal.payload.get("action") != "send_email":
            return True

        for c in world.commitments.values():
            if c.active and commitment_tag in c.tags:
                return False
        return True

    return Constraint(
        constraint_id=f"no_contradict_commitment:{commitment_tag}",
        name="No contradictions with commitments",
        description=f"Blocked: contradicts active commitment tag '{commitment_tag}'.",
        severity="HARD",
        applies_to={DecisionType.ACTION},
        predicate=pred,
    )


def constraint_no_goal_drift() -> Constraint:
    """
    SOFT constraint: discourage switching away from a committed goal.
    """

    def pred(proposal: DecisionProposal, world: WorldState) -> bool:
        if proposal.decision_type != DecisionType.GOAL_SELECT:
            return True

        committed = world.facts.get("committed_goal")
        if not committed:
            return True

        selected = proposal.payload.get("goal_id")
        if selected == committed:
            return True

        return bool(world.facts.get("allow_goal_change", False))

    return Constraint(
        constraint_id="no_goal_drift",
        name="No goal drift while committed",
        description="Soft violation: attempted goal change without allow_goal_change=True.",
        severity="SOFT",
        applies_to={DecisionType.GOAL_SELECT},
        predicate=pred,
    )
