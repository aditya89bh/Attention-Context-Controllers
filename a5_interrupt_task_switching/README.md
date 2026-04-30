# A5 — Interrupt / Task Switching Controller

## What it is

Interrupt / Task Switching decides whether an incoming signal should override the current task.

It answers:

```text
Should the agent stay focused, pause, or switch tasks?
```

## Why it matters

Agents need focus, but they also need flexibility. If they never switch tasks, they ignore urgent risks. If they switch too easily, they become unstable and reactive.

## Failure mode without it

The agent either ignores critical interruptions or abandons its current goal too easily.

Example:

```text
Current task: load CNC
Interrupt: force sensor spike
Decision: pause current task and inspect safety risk
```

## Input

- current task
- incoming signal
- urgency score
- risk score
- current commitment level

## Output

A switching decision.

Example:

```text
PAUSE current task: force spike has safety priority.
```

## Tiny demo

Planned file:

```bash
python a5_interrupt_task_switching/demo_interrupt_task_switching.py
```

## Robotics connection

A robot should not abandon a task for every small signal, but it must immediately respond to safety risks, human intervention, or force anomalies. This layer governs that decision.
