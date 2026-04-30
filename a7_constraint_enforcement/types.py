"""A7 Constraint Enforcement core data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Set


class DecisionType(str, Enum):
    """Types of decisions that can be validated by A7."""

    ACTION = "ACTION"
    GOAL_SELECT = "GOAL_SELECT"
    PLAN_STEP = "PLAN_STEP"
    MESSAGE = "MESSAGE"


class EnforcementMode(str, Enum):
    """How strictly constraints should be enforced."""

    STRICT = "STRICT"
    SOFT = "SOFT"
    AUDIT = "AUDIT"


@dataclass(frozen=True)
class DecisionProposal:
    """A proposed decision or action that should be checked before execution."""

    decision_id: str
    decision_type: DecisionType
    payload: Dict[str, Any]
    tags: Set[str] = field(default_factory=set)


@dataclass
class Commitment:
    """An active promise, lock, or behavioral commitment."""

    commitment_id: str
    description: str
    tags: Set[str] = field(default_factory=set)
    active: bool = True


@dataclass
class WorldState:
    """Minimal state needed for constraint enforcement."""

    facts: Dict[str, Any] = field(default_factory=dict)
    commitments: Dict[str, Commitment] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)

    def add_commitment(self, commitment: Commitment) -> None:
        self.commitments[commitment.commitment_id] = commitment

    def record(self, event: Dict[str, Any]) -> None:
        self.history.append(event)


@dataclass(frozen=True)
class Constraint:
    """A named invariant or policy rule."""

    constraint_id: str
    name: str
    description: str
    severity: str
    applies_to: Set[DecisionType]
    predicate: Callable[[DecisionProposal, WorldState], bool]
    required_tags: Set[str] = field(default_factory=set)


@dataclass(frozen=True)
class ConstraintResult:
    """Result of evaluating one constraint."""

    constraint_id: str
    ok: bool
    severity: str
    message: str


@dataclass(frozen=True)
class ValidationReport:
    """Structured result returned by A7 validation."""

    proposal: DecisionProposal
    allowed: bool
    mode: EnforcementMode
    results: List[ConstraintResult]
    penalties: Dict[str, float]
    notes: Dict[str, Any] = field(default_factory=dict)
