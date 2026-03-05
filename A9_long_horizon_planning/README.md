# A9 — Long-Horizon Planning & Commitment Controller

**One-liner:** A deterministic control layer that creates multi-step plans, simulates them, selects the best plan, and maintains commitment over time with abandonment and replanning logic.

---

## Architectural Position

This repository is organized as a layered agent controller stack. **A9** sits after goal selection/arbitration and before step-level enforcement and monitoring.

- **A1** Context Framing
- **A2** Attention Budgeting
- **A3** Salience Memory Access
- **A4** Temporal Context
- **A5** Task Switching
- **A6** Goal Arbitration
- **A7** Consistency & Constraint Enforcement
- **A8** Self-Monitoring & Introspection
- **A9** Long-Horizon Planning & Commitment ← **Current Layer**
- **A10** Identity & Value Stabilization

---

## Why A9 Exists

Without A9, an agent tends to be **short-horizon and reactive**:

- it switches tasks frequently
- it over-responds to local noise
- it lacks durable execution continuity

A9 introduces a core primitive:

> **Temporal Strategic Continuity** — the ability to pick a plan and *stick with it* long enough to execute, while still being able to abandon and replan when progress collapses.

---

## What A9 Does

A9 provides a deterministic planning + commitment loop:

- **Goal decomposition** via a goal tree
- **Candidate plan generation** (multiple action sequences)
- **Plan simulation** using a deterministic toy world model
- **Plan selection** based on scoring
- **Commitment tracking** so the agent does not switch plans prematurely
- **Checkpoints and abandonment logic** when repeated failures occur
- **Replanning** when commitment drops below a threshold

**Non-goals:**

- No machine learning training
- No dependence on LLM internals
- No probabilistic policy learning

This is **pure Python system design** for controllable, debuggable behavior.

---

## Core Concepts

- **Goal:** a target state to achieve
- **GoalTree:** hierarchical decomposition of a goal into subgoals
- **Plan:** an ordered sequence of actions/steps
- **Simulator:** a deterministic scoring model that evaluates candidate plans
- **Commitment:** a persistence mechanism that resists premature plan switching
- **Abandonment:** dropping a plan after repeated failures or low progress

---

## Control Flow

1) Receive a goal
2) Construct a goal tree
3) Generate candidate plans up to a depth limit
4) Simulate each plan and compute a score
5) Select the highest-scoring plan
6) Execute steps sequentially while commitment remains high
7) If failures repeat, commitment decays
8) If commitment drops below threshold, abandon the plan and replan

---

## Demo

`demo/demo_planning.py` is intended to demonstrate the end-to-end loop:

- goal tree creation
- plan generation
- simulation + scoring
- selected plan
- commitment decay
- replanning trigger

Run from the repo root:

```bash
python3 A9_long_horizon_planning/demo/demo_planning.py
```

---

## Project Structure

```
A9_long_horizon_planning/
  a9/
    __init__.py
    types.py
    goal_tree.py
    planner.py
    simulator.py
  demo/
    demo_planning.py
  README.md
```

---

## Integration with A6–A8

- **A6** selects *which goal* should be pursued.
- **A9** generates and manages the plan for that goal.
- **A7** validates each step before execution (constraints, safety, invariants).
- **A8** monitors execution history and can trigger replanning if instability is detected.

A simple way to think about it:

- **A6 decides what matters**
- **A9 decides how to get it done**
- **A7 decides whether each step is allowed**
- **A8 decides whether things are going off the rails**

---

## License

MIT
