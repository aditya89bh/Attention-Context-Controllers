"""A10 Identity and Value Stabilization core data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class ValueCategory(str, Enum):
    """Categories of values an agent can hold."""

    SAFETY = "SAFETY"
    EFFICIENCY = "EFFICIENCY"
    ACCURACY = "ACCURACY"
    TRANSPARENCY = "TRANSPARENCY"
    RESOURCE_USE = "RESOURCE_USE"


@dataclass(frozen=True)
class IdentityProfile:
    """Persistent identity definition describing the agent and its value priorities."""

    agent_id: str
    description: str
    value_weights: Dict[ValueCategory, float]
    created_at: str


@dataclass(frozen=True)
class ValueScore:
    """Score assigned to a value category during evaluation."""

    category: ValueCategory
    score: float
    reason: str


@dataclass(frozen=True)
class ValueEvaluation:
    """Combined value evaluation results for a plan."""

    plan_id: str
    scores: List[ValueScore]
    total_score: float
    notes: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ValueConfig:
    """Configuration controlling how strongly values influence decisions."""

    normalization_factor: float = 1.0
    bias_strength: float = 1.0
