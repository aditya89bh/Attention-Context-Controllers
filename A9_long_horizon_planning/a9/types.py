"""A9 planning layer — core data structures.

This module intentionally contains **only**:
- dataclasses
- enums

No planning/search/simulation logic should live here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PlanStatus(str, Enum):
    """Lifecycle status of a plan."""

    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ABANDONED = "ABANDONED"
    COMPLETED = "COMPLETED"


@dataclass(frozen=True)
class Goal:
    """A goal the agent wants to achieve.

    `priority` is a simple scalar used for ordering/selection.
    `tags` allows light categorization (e.g., "robotics", "ops", "urgent").
    """

    goal_id: str
    description: str
    priority: float = 1.0
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Action:
    """An atomic action used inside a plan.

    `params` captures structured arguments.
    `cost` and `risk` are scalar estimates used for scoring.
    """

    name: str
    params: dict[str, Any] = field(default_factory=dict)
    cost: float = 1.0
    risk: float = 0.0


@dataclass(frozen=True)
class PlanStep:
    """A single step in a plan."""

    step_id: str
    action: Action
    expected_outcome: str


@dataclass
class Plan:
    """A multi-step plan tied to a goal.

    `current_step_index` points to the next step to execute.
    `commitment_strength` controls persistence vs. abandoning/replanning.
    """

    plan_id: str
    goal_id: str
    steps: list[PlanStep]
    status: PlanStatus
    current_step_index: int = 0
    commitment_strength: float = 1.0


@dataclass(frozen=True)
class SimResult:
    """Result of simulating/scoring a plan."""

    plan_id: str
    score: float
    total_cost: float
    risk_score: float
    success: bool
    notes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlannerConfig:
    """Configuration knobs for planning + commitment control."""

    max_plan_depth: int = 5
    beam_width: int = 3
    commitment_decay: float = 0.1
    abandonment_threshold: float = 0.3
