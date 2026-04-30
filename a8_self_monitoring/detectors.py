from __future__ import annotations

from typing import Dict, List, Tuple

from .types import (
    Issue,
    IssueType,
    Intervention,
    MonitorConfig,
    Severity,
    event_signature,
)


def _recent(events: List[Dict], window: int) -> List[Dict]:
    """Return the last window events."""
    if window <= 0:
        return []
    return events[-window:]


def detect_loop(events: List[Dict], cfg: MonitorConfig) -> Tuple[List[Issue], List[Intervention]]:
    """Detect repeated identical behavior signatures."""
    recent_events = _recent(events, cfg.window)
    signatures = [event_signature(event) for event in recent_events]

    counts: Dict[str, int] = {}
    for signature in signatures:
        counts[signature] = counts.get(signature, 0) + 1

    if not counts:
        return [], []

    top_signature = max(counts, key=lambda key: counts[key])
    top_count = counts[top_signature]

    if top_count < cfg.loop_repetition_threshold:
        return [], []

    severity = Severity.HIGH if top_count >= cfg.loop_repetition_threshold + 2 else Severity.MEDIUM

    issues = [
        Issue(
            issue_type=IssueType.LOOP,
            severity=severity,
            message=f"Loop detected: {top_signature} repeated {top_count} times.",
            signature=top_signature,
            evidence={"count": top_count, "window": len(recent_events), "signatures": signatures},
        )
    ]

    interventions = [
        Intervention(
            name="pause_and_replan",
            reason=f"Loop detected on {top_signature}.",
            params={"loop_signature": top_signature},
        )
    ]

    return issues, interventions


def detect_thrash(events: List[Dict], cfg: MonitorConfig) -> Tuple[List[Issue], List[Intervention]]:
    """Detect excessive switching between different behavior signatures."""
    recent_events = _recent(events, cfg.window)
    signatures = [event_signature(event) for event in recent_events]

    if len(signatures) < 3:
        return [], []

    switches = 0
    for index in range(1, len(signatures)):
        if signatures[index] != signatures[index - 1]:
            switches += 1

    if switches < cfg.thrash_switch_threshold:
        return [], []

    severity = Severity.HIGH if switches >= cfg.thrash_switch_threshold + 2 else Severity.MEDIUM

    issues = [
        Issue(
            issue_type=IssueType.THRASH,
            severity=severity,
            message=f"Thrash detected: {switches} switches in recent behavior.",
            signature="thrash:switches",
            evidence={"switches": switches, "window": len(recent_events), "signatures": signatures},
        )
    ]

    interventions = [
        Intervention(
            name="stabilize_focus",
            reason="Thrashing detected. Lock one goal or task briefly.",
            params={"switches": switches, "lock_steps": 3},
        )
    ]

    return issues, interventions


def detect_repeated_violations(events: List[Dict], cfg: MonitorConfig) -> Tuple[List[Issue], List[Intervention]]:
    """Detect repeated blocked proposals caused by the same constraint."""
    recent_events = _recent(events, cfg.window)

    violated: List[str] = []
    for event in recent_events:
        if event.get("type") != "proposal_blocked":
            continue
        results = event.get("results") or []
        for result in results:
            if not result.get("ok", True):
                violated.append(result.get("constraint_id", "unknown"))

    counts: Dict[str, int] = {}
    for constraint_id in violated:
        counts[constraint_id] = counts.get(constraint_id, 0) + 1

    issues: List[Issue] = []
    interventions: List[Intervention] = []

    for constraint_id, count in counts.items():
        if count < cfg.violation_repeat_threshold:
            continue

        severity = Severity.HIGH if count >= cfg.violation_repeat_threshold + 1 else Severity.MEDIUM

        issues.append(
            Issue(
                issue_type=IssueType.REPEATED_VIOLATION,
                severity=severity,
                message=f"Repeated violation: {constraint_id} triggered {count} times.",
                signature=f"constraint:{constraint_id}",
                evidence={"constraint_id": constraint_id, "count": count, "window": len(recent_events)},
            )
        )
        interventions.append(
            Intervention(
                name="escalate_or_adjust",
                reason=f"Repeatedly hitting {constraint_id}. Ask for approval or revise strategy.",
                params={"constraint_id": constraint_id, "count": count},
            )
        )

    return issues, interventions
