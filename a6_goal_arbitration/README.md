# A6 — Goal Arbitration Controller

## What it is

Goal Arbitration chooses which goal should be active when multiple goals compete.

It answers:

```text
Which goal should the agent pursue now?
```

## Why it matters

Agents often face competing goals: finish the task, reduce risk, answer the operator, preserve resources, or recover from failure. Without arbitration, goal selection becomes inconsistent.

## Failure mode without it

The agent jumps between goals without a clear priority rule.

Example:

```text
Goal 1: finish CNC loading
Goal 2: recover failed pickup
Goal 3: answer operator
Goal 4: inspect force anomaly
```

With goal arbitration, the active goal may become:

```text
Recover failed pickup safely.
```

## Input

- candidate goals
- context frame
- attention budget
- risk level
- urgency level
- value preferences

## Output

One active goal, plus optionally deferred goals.

Example:

```text
Active goal: recover failed pickup safely
Deferred goal: operator status update
Deferred goal: normal loading continuation
```

## Tiny demo

Planned file:

```bash
python a6_goal_arbitration/demo_goal_arbitration.py
```

## Robotics connection

A robot should know when safety recovery outranks speed, when operator communication outranks task continuation, and when normal execution can resume. Goal arbitration makes that priority decision explicit.
