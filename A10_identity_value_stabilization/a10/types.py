"""A10 — core data structures.

This file intentionally contains only dataclasses/enums-like structures.
No business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PolicyConstraint:
    """A non-negotiable rule or boundary.

    Examples:
    - "Do not reveal secrets"
    - "Do not take external actions without confirmation"
    """

    constraint_id: str
    text: str
    severity: str = "hard"  # hard | soft


@dataclass(frozen=True)
class AgentIdentity:
    """Stable identity settings for an agent."""

    name: str
    role: str
    audience: str
    tone: str = "direct, competent, low-fluff"


@dataclass(frozen=True)
class AgentValues:
    """Prioritized values that guide trade-offs."""

    values: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DriftSignal:
    """A detected mismatch between current behavior and the identity/values/policy profile."""

    signal_id: str
    description: str
    score: float = 0.0
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvaluationResult:
    """Result of evaluating a candidate response against A10 constraints."""

    ok: bool
    drift_score: float
    signals: list[DriftSignal] = field(default_factory=list)
    notes: dict[str, Any] = field(default_factory=dict)
