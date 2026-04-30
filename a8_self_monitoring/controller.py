from __future__ import annotations

from typing import Dict, List, Optional

from .detectors import detect_loop, detect_repeated_violations, detect_thrash
from .types import IntrospectionReport, MonitorConfig


class SelfMonitoringController:
    """
    A8 Self-Monitoring Controller.

    Consumes behavior events and emits introspection issues plus interventions.
    """

    def __init__(self, config: Optional[MonitorConfig] = None):
        self.config = config or MonitorConfig()

    def analyze(self, events: List[Dict]) -> IntrospectionReport:
        """Run all detectors over recent behavior events."""
        issues = []
        interventions = []

        detected_issues, suggested_interventions = detect_loop(events, self.config)
        issues.extend(detected_issues)
        interventions.extend(suggested_interventions)

        detected_issues, suggested_interventions = detect_thrash(events, self.config)
        issues.extend(detected_issues)
        interventions.extend(suggested_interventions)

        detected_issues, suggested_interventions = detect_repeated_violations(events, self.config)
        issues.extend(detected_issues)
        interventions.extend(suggested_interventions)

        return IntrospectionReport(
            issues=issues,
            interventions=interventions,
            notes={
                "window": self.config.window,
                "events_seen": len(events),
            },
        )
