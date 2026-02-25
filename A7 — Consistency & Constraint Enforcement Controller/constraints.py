"""
A7 — Built-in Constraints Library (constraints.py)

This module contains reusable constraint constructors that plug into the
A7 ConsistencyController.

Why separate this file?
- Keeps controller.py focused on enforcement policy, not domain rules
- Makes it easy for contributors to add constraints without touching core logic
- Scales naturally as constraints grow (safety, compliance, budgets, etc.)
"""

from __future__ import annotations

from .types import Constraint, DecisionProposal, DecisionType, WorldState


def constraint_require_human_for_irreversible() -> Constraint:
    """
    Safety gate: If a proposal is tagged "irreversible", require explicit approval.

    Required world fact:
      world.facts["human_approved"] == True

    Typical use:
      - deleting data
      - financial transactions
      - external communications
      - physical robot actions that can't be undone
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

    Default example:
      - If an active commitment has tag "no_send_email"
      - Block action == "send_email"

    This pattern generalizes well:
      - no_external_calls
      - no_spend_money
      - stay_on_goal:g1
      - do_not_contact:alice
    """

    def pred(proposal: DecisionProposal, world: WorldState) -> bool:
        if proposal.decision_type != DecisionType.ACTION:
            return True

        # Default behavior: only constrain send_email
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

    If:
      world.facts["committed_goal"] exists
    and:
      proposal selects a different goal_id
    then:
      violation unless world.facts["allow_goal_change"] == True

    Why SOFT?
      - Goal switches might be allowed but should carry friction/penalty.
      - A6 can incorporate this penalty during arbitration.
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
