%%bash
cat > A8_self_monitoring_introspection/demo/demo_repeat_violation.py << 'PY'
from a8.controller import SelfMonitoringController
from a8.types import MonitorConfig

def main():
    cfg = MonitorConfig(window=12, violation_repeat_threshold=3)
    mon = SelfMonitoringController(cfg)

    events = []
    for i in range(4):
        events.append({
            "type": "proposal_blocked",
            "proposal": f"p{i}",
            "payload": {"action": "delete_file"},
            "results": [
                {"constraint_id": "require_human_for_irreversible", "ok": False, "severity": "HARD", "message": "blocked"}
            ],
            "penalties": {"require_human_for_irreversible": 10.0},
        })

    report = mon.analyze(events)

    print("issues:", [(x.issue_type, x.severity, x.signature, x.evidence.get("count")) for x in report.issues])
    print("interventions:", [x.name for x in report.interventions])

if __name__ == "__main__":
    main()
PY
