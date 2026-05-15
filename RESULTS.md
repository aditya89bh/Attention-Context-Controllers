# Results

This file summarizes the verified behavior of the Attention & Context Controllers repository.

The repository contains deterministic mini demos for A1-A10 and one full integrated cognitive control loop.

---

## Verified Commands

The following commands were run locally on macOS inside a Python virtual environment:

```bash
python run_all_demos.py
python -m pytest tests/test_smoke.py
```

Captured outputs are stored in:

```text
results/run_all_demos_output.txt
results/full_cognitive_control_loop_output.txt
results/test_smoke_output.txt
```

---

## Verification Summary

| Check | Result |
|---|---|
| A1-A10 individual demos | Passed |
| Full A1-A10 integrated demo | Passed |
| Smoke tests | 4 passed |
| Output capture | Complete |
| External API dependency | None |
| GPU dependency | None |

---

## Controller Evidence Matrix

| Layer | Demo | What it proves | Evidence |
|---|---|---|---|
| A1 | Context Framing | Raw robot/task signals become a compact task frame | `results/run_all_demos_output.txt` |
| A2 | Attention Budgeting | Reasoning effort is allocated across concerns | `results/run_all_demos_output.txt` |
| A3 | Salience Memory Access | Relevant memories are selected and irrelevant memories ignored | `results/run_all_demos_output.txt` |
| A4 | Temporal Context | Past, present, and future are separated | `results/run_all_demos_output.txt` |
| A5 | Interrupt / Task Switching | Urgent risk can override current focus | `results/run_all_demos_output.txt` |
| A6 | Goal Arbitration | One active goal is selected from competing goals | `results/run_all_demos_output.txt` |
| A7 | Constraint Enforcement | Proposed actions are checked before execution | `results/run_all_demos_output.txt` |
| A8 | Self-Monitoring | Loops and repeated violations are detected | `results/run_all_demos_output.txt` |
| A9 | Long-Horizon Planning | A plan is generated, selected, and committed | `results/run_all_demos_output.txt` |
| A10 | Identity & Value Stabilization | Value weights bias plan selection | `results/run_all_demos_output.txt` |
| Full loop | Integrated Cognitive Control Loop | A single CNC failed-pickup scenario flows through A1-A10 | `results/full_cognitive_control_loop_output.txt` |

---

## Full Loop Scenario

The integrated demo uses a CNC failed-pickup scenario:

```text
failed pickup -> tray drift memory -> recovery context -> safety-aware retry plan
```

The full loop demonstrates:

1. context framing
2. attention allocation
3. salient memory selection
4. temporal separation
5. interrupt handling
6. goal arbitration
7. constraint validation
8. self-monitoring
9. long-horizon planning
10. value-biased plan selection

---

## Smoke Test Coverage

The smoke tests verify import and minimal behavior for:

- A7 Constraint Enforcement
- A8 Self-Monitoring
- A9 Long-Horizon Planning
- A10 Identity & Value Stabilization

Current smoke test result:

```text
4 passed
```

---

## Current Limits

This repository is a research-practice artifact, not a production framework.

Current limitations:

- tests are smoke-level, not exhaustive
- A1-A6 are deterministic demo modules, not full production controllers
- no real LLM runtime integration
- no ROS or real robot integration
- no benchmark suite
- no production API stability guarantee

---

## Interpretation

The repository is now verified as a runnable portfolio-grade cognitive-control research prototype.

It demonstrates the concept clearly, but it does not claim to be a production agent-control system.
