from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class IssueType(str, Enum):
    LOOP = "LOOP"
    THRASH = "THRASH"
    REPEATED_VIOLATION = "REPEATED_VIOLATION"
    LOW_PROGRESS = "LOW_PROGRESS"


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class MonitorConfig:
    window: int = 12
    loop_repetition_threshold: int = 4
    thrash_switch_threshold: int = 6
    violation_repeat_threshold: int = 3


@dataclass
class Issue:
    issue_type: IssueType
    severity: Severity
    message: str
    signature: str
    evidence: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Intervention:
    name: str
    reason: str
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IntrospectionReport:
    issues: List[Issue] = field(default_factory=list)
    interventions: List[Intervention] = field(default_factory=list)
    notes: Dict[str, Any] = field(default_factory=dict)


def event_signature(event: Dict[str, Any]) -> str:
    """Create a stable signature for behavior trace analysis."""
    event_type = event.get("type", "unknown")

    if event_type in ("proposal_accepted", "proposal_blocked"):
        payload = event.get("payload") or {}
        action = payload.get("action")
        if action:
            return f"action:{action}"
        proposal_id = event.get("proposal")
        if proposal_id:
            return f"proposal:{proposal_id}"
        return "proposal:unknown"

    if event_type in ("commitment_added", "commitment_retracted"):
        commitment_id = event.get("commitment", "unknown")
        return f"commitment:{commitment_id}"

    return f"event:{event_type}"
