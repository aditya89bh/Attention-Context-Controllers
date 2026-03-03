%%bash
cat > A8_self_monitoring_introspection/demo/demo_thrashing.py << 'PY'
from a8.controller import SelfMonitoringController
from a8.types import MonitorConfig

def main():
    cfg = MonitorConfig(window=10, thrash_switch_threshold=6)
    mon = SelfMonitoringController(cfg)

    events = []
    actions = ["plan", "search"] * 6
    for i, a in enumerate(actions):
        events.append({"type": "proposal_accepted", "proposal": f"p{i}", "payload": {"action": a}})

    report = mon.analyze(events)

    print("issues:", [(x.issue_type, x.severity, x.signature) for x in report.issues])
    print("interventions:", [x.name for x in report.interventions])

if __name__ == "__main__":
    main()
PY
