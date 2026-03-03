%%bash
cat > A8_self_monitoring_introspection/demo/demo_looping.py << 'PY'
from a8.controller import SelfMonitoringController
from a8.types import MonitorConfig

def main():
    cfg = MonitorConfig(window=10, loop_repetition_threshold=4)
    mon = SelfMonitoringController(cfg)

    events = []
    for i in range(6):
        events.append({"type": "proposal_accepted", "proposal": f"p{i}", "payload": {"action": "search"}})

    report = mon.analyze(events)

    print("issues:", [(x.issue_type, x.severity, x.signature) for x in report.issues])
    print("interventions:", [x.name for x in report.interventions])

if __name__ == "__main__":
    main()
PY
