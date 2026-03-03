%%bash
cat > A8_self_monitoring_introspection/a8/controller.py << 'PY'
from __future__ import annotations

from typing import Dict, List, Optional

from .types import IntrospectionReport, MonitorConfig
from .detectors import detect_loop, detect_thrash, detect_repeated_violations


class SelfMonitoringController:
    """
    A8 — Self-Monitoring & Introspection Controller

    Consumes:
      - events: list[dict] (typically A7 WorldState.history)

    Produces:
      - IntrospectionReport (issues + interventions)

    A8 is intentionally deterministic and model-agnostic:
      - no ML training
      - no LLM internals
      - pattern detection over behavior traces only
    """

    def __init__(self, config: Optional[MonitorConfig] = None):
        self.cfg = config or MonitorConfig()

    def analyze(self, events: List[Dict]) -> IntrospectionReport:
        """
        Run all detectors over the recent event window and merge results.
        """
        issues = []
        interventions = []

        i, a = detect_loop(events, self.cfg)
        issues.extend(i)
        interventions.extend(a)

        i, a = detect_thrash(events, self.cfg)
        issues.extend(i)
        interventions.extend(a)

        i, a = detect_repeated_violations(events, self.cfg)
        issues.extend(i)
        interventions.extend(a)

        notes = {
            "window": self.cfg.window,
            "events_seen": len(events),
        }

        return IntrospectionReport(issues=issues, interventions=interventions, notes=notes)
PY
echo "controller.py written"
