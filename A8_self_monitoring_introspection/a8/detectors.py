%%bash
cat > A8_self_monitoring_introspection/a8/detectors.py << 'PY'
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
    """Return last `window` events (or fewer)."""
    if window <= 0:
        return []
    return events[-window:]


def detect_loop(events: List[Dict], cfg: MonitorConfig) -> Tuple[List[Issue], List[Intervention]]:
    """
    LOOP: same signature repeats too many times in the sliding window.
    """
    evs = _recent(events, cfg.window)
    sigs = [event_signature(e) for e in evs]

    counts: Dict[str, int] = {}
    for s in sigs:
        counts[s] = counts.get(s, 0) + 1

    if not counts:
        return [], []

    top_sig = max(counts, key=lambda k: counts[k])
    top_count = counts[top_sig]

    if top_count < cfg.loop_repetition_threshold:
        return [], []

    severity = Severity.HIGH if top_count >= cfg.loop_repetition_threshold + 2 else Severity.MEDIUM

    issues = [
        Issue(
            issue_type=IssueType.LOOP,
            severity=severity,
            message=f"Loop detected: '{top_sig}' repeated {top_count} times in last {len(evs)} events.",
            signature=top_sig,
            evidence={"count": top_count, "window": len(evs), "signatures": sigs},
        )
    ]

    interventions = [
        Intervention(
            name="pause_and_replan",
            reason=f"Loop on '{top_sig}'. Pause and generate an alternative strategy.",
            params={"loop_signature": top_sig},
        )
    ]

    return issues, interventions


def detect_thrash(events: List[Dict], cfg: MonitorConfig) -> Tuple[List[Issue], List[Intervention]]:
    """
    THRASH: rapid switching between different signatures.

    We count the number of switches in the signature sequence.
    """
    evs = _recent(events, cfg.window)
    sigs = [event_signature(e) for e in evs]

    if len(sigs) < 3:
        return [], []

    switches = 0
    for i in range(1, len(sigs)):
        if sigs[i] != sigs[i - 1]:
            switches += 1

    if switches < cfg.thrash_switch_threshold:
        return [], []

    severity = Severity.HIGH if switches >= cfg.thrash_switch_threshold + 2 else Severity.MEDIUM

    issues = [
        Issue(
            issue_type=IssueType.THRASH,
            severity=severity,
            message=f"Thrash detected: {switches} switches in last {len(evs)} events.",
            signature="thrash:switches",
            evidence={"switches": switches, "window": len(evs), "signatures": sigs},
        )
    ]

    interventions = [
        Intervention(
            name="stabilize_focus",
            reason="Thrash detected. Lock one goal/task briefly to regain stability.",
            params={"switches": switches, "lock_steps": 3},
        )
    ]

    return issues, interventions


def detect_repeated_violations(events: List[Dict], cfg: MonitorConfig) -> Tuple[List[Issue], List[Intervention]]:
    """
    REPEATED_VIOLATION: repeated proposal_blocked events for the same constraint_id.

    Expects A7-style blocked event format:
      event["results"] = [{constraint_id, ok, severity, message}, ...]
    """
    evs = _recent(events, cfg.window)

    violated: List[str] = []
    for e in evs:
        if e.get("type") != "proposal_blocked":
            continue
        results = e.get("results") or []
        for r in results:
            if not r.get("ok", True):
                violated.append(r.get("constraint_id", "unknown"))

    counts: Dict[str, int] = {}
    for cid in violated:
        counts[cid] = counts.get(cid, 0) + 1

    issues: List[Issue] = []
    interventions: List[Intervention] = []

    for cid, n in counts.items():
        if n < cfg.violation_repeat_threshold:
            continue

        severity = Severity.HIGH if n >= cfg.violation_repeat_threshold + 1 else Severity.MEDIUM

        issues.append(
            Issue(
                issue_type=IssueType.REPEATED_VIOLATION,
                severity=severity,
                message=f"Repeated violation: '{cid}' triggered {n} times in last {len(evs)} events.",
                signature=f"constraint:{cid}",
                evidence={"constraint_id": cid, "count": n, "window": len(evs)},
            )
        )
        interventions.append(
            Intervention(
                name="escalate_or_adjust",
                reason=f"Repeatedly hitting '{cid}'. Ask for missing approvals or revise plan/strategy.",
                params={"constraint_id": cid, "count": n},
            )
        )

    return issues, interventions
PY
echo "detectors.py written"
