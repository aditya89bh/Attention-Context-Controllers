"""Run all Attention & Context Controller demos.

Run from repo root:
    python run_all_demos.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


DEMOS = [
    "a1_context_framing/demo_context_framing.py",
    "a2_attention_budgeting/demo_attention_budgeting.py",
    "a3_salience_memory_access/demo_salience_memory_access.py",
    "a4_temporal_context/demo_temporal_context.py",
    "a5_interrupt_task_switching/demo_interrupt_task_switching.py",
    "a6_goal_arbitration/demo_goal_arbitration.py",
    "a7_constraint_enforcement/demo_constraint_enforcement.py",
    "a8_self_monitoring/demo_self_monitoring.py",
    "a9_long_horizon_planning/demo_long_horizon_planning.py",
    "a10_identity_value_stabilization/demo_identity_value_stabilization.py",
    "examples/full_cognitive_control_loop.py",
]


def main() -> None:
    root = Path(__file__).resolve().parent
    failures: list[str] = []

    print("Running all Attention & Context Controller demos...\n")

    for demo in DEMOS:
        print("=" * 80)
        print(f"RUNNING: {demo}")
        print("=" * 80)
        result = subprocess.run([sys.executable, str(root / demo)], cwd=root)
        if result.returncode != 0:
            failures.append(demo)
        print()

    if failures:
        print("Demo failures:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("All demos completed successfully.")


if __name__ == "__main__":
    main()
