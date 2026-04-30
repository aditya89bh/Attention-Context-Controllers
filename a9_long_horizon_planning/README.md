# A9 — Long-Horizon Planning Controller

## What it is

Long-Horizon Planning creates multi-step plans, simulates them, selects the best plan, and maintains commitment over time with abandonment and replanning logic.

It answers:

```text
How should the agent pursue the selected goal across multiple steps?
```

## Why it matters

Without long-horizon planning, agents become short-horizon and reactive. They switch tasks frequently, over-respond to local noise, and fail to maintain execution continuity.

A9 introduces temporal strategic continuity: the ability to choose a plan and stay with it long enough to execute, while still being able to abandon and replan when progress collapses.

## Failure mode without it

The agent may:

- switch plans too early
- react to every new signal
- fail to complete multi-step goals
- continue bad plans without abandonment logic
- replan too often or too late

## Input

- selected goal
- action candidates
- planning configuration
- risk and cost estimates
- commitment thresholds

## Output

A selected and committed plan.

Example:

```text
Plan: inspect tray -> adjust offset -> retry pickup -> verify grasp
Commitment: active
Abandonment threshold: 0.3
```

## Existing implementation notes

This layer currently includes:

- goal data structures
- plan and plan-step data structures
- deterministic plan simulator
- deterministic candidate plan generation
- plan selection
- commitment decay
- abandonment and replanning hooks

No ML, no LLM API, and no external dependencies are required.

## Tiny demo

Planned normalized demo file:

```bash
python a9_long_horizon_planning/demo_long_horizon_planning.py
```

## Robotics connection

A robot recovering from a failed pickup should not randomly jump between recovery strategies. A9 helps it commit to a plan such as inspect tray, adjust offset, retry pickup, and verify grasp, while still allowing abandonment if failures continue.
