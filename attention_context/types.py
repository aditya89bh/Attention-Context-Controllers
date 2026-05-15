"""Shared data types for the Attention & Context Controllers package."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class Signal:
    source: str
    content: str
    urgency: int
    risk: int
    relevance: int


@dataclass(frozen=True)
class MemoryCandidate:
    memory_id: str
    content: str
    relevance: int
    recency: int
    risk_connection: int
    goal_fit: int


@dataclass(frozen=True)
class GoalCandidate:
    goal_id: str
    description: str
    relevance: int
    urgency: int
    risk_reduction: int
    value_alignment: int


@dataclass(frozen=True)
class ControlLoopResult:
    context_frame: Dict[str, Any]
    attention_budget: Dict[str, int]
    selected_memories: List[Tuple[MemoryCandidate, float]]
    temporal_context: Dict[str, List[str]]
    interrupt_decision: Dict[str, Any]
    active_goal: GoalCandidate
    constraint_report: Any
    self_monitoring_report: Any
    committed_plan: Any
    value_aligned_plan: Any
    notes: Dict[str, Any] = field(default_factory=dict)
