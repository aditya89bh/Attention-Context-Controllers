# Architecture: A1-A10 Cognitive Control Stack

This document explains the architecture behind the Attention & Context Controllers repo.

The goal of the stack is to make agent cognition more controlled, focused, and explainable.

This is not a production architecture. It is a study architecture for understanding the primitives behind long-horizon agents.

---

## Core Problem

Most agent systems have access to:

- memory
- tools
- plans
- prompts
- long context windows

But they often lack explicit control over:

- what matters right now
- which memories should be retrieved
- which signals should be ignored
- when to interrupt a plan
- when to stay committed
- when to replan
- how values should bias decisions

The A1-A10 stack breaks these control problems into small primitives.

---

## Full Stack

```text
Raw Signals
  -> A1 Context Framing
  -> A2 Attention Budgeting
  -> A3 Salience Memory Access
  -> A4 Temporal Context
  -> A5 Interrupt / Task Switching
  -> A6 Goal Arbitration
  -> A7 Constraint Enforcement
  -> A8 Self-Monitoring
  -> A9 Long-Horizon Planning
  -> A10 Identity & Value Stabilization
  -> Action
```

---

## Layer Responsibilities

| Layer | Controller | Responsibility |
|---|---|---|
| A1 | Context Framing | Convert raw signals into a structured task frame |
| A2 | Attention Budgeting | Allocate limited reasoning effort across competing concerns |
| A3 | Salience Memory Access | Retrieve memories based on relevance, urgency, and risk |
| A4 | Temporal Context | Separate past recall, present execution, and future simulation |
| A5 | Interrupt / Task Switching | Decide whether an incoming signal should override current focus |
| A6 | Goal Arbitration | Choose which goal should be active when goals compete |
| A7 | Constraint Enforcement | Check safety, consistency, and invariants before action |
| A8 | Self-Monitoring | Detect drift, instability, and confidence collapse |
| A9 | Long-Horizon Planning | Generate, select, commit to, abandon, and replan multi-step plans |
| A10 | Identity & Value Stabilization | Keep decisions aligned with persistent values and identity |

---

## Robotics Example

Scenario: A robot is loading a CNC machine and fails to pick up a part.

### Raw Signals

- current task: load CNC
- event: failed pickup
- memory: tray drift happened yesterday
- operator message: asking for status
- force sensor: slight anomaly
- background log: unrelated maintenance note

### A1 Context Framing

The system frames the situation as:

```text
Recovery mode after failed pickup during CNC loading.
```

### A2 Attention Budgeting

The system allocates reasoning budget:

```text
Failure recovery: 60
Operator communication: 20
Logging: 20
```

### A3 Salience Memory Access

Relevant memory retrieved:

```text
Previous tray drift episode.
```

Irrelevant background log is ignored.

### A4 Temporal Context

```text
Past: tray drift episode
Present: failed pickup
Future: retry with offset
```

### A5 Interrupt Handling

The force anomaly is checked. If risk is high, it overrides the current task.

### A6 Goal Arbitration

The active goal becomes:

```text
Recover safe pickup.
```

### A7 Constraint Enforcement

The controller blocks unsafe retries and enforces:

```text
Reduced speed.
Collision zone avoidance.
```

### A8 Self-Monitoring

Confidence is lowered because the previous plan failed.

### A9 Long-Horizon Planning

The planner commits to:

```text
Inspect tray -> adjust offset -> retry pickup -> verify grasp
```

### A10 Identity & Value Stabilization

The value layer biases the decision toward:

```text
Safety over speed.
```

---

## Why This Stack Matters

Memory alone does not create intelligence.

A useful agent must decide:

- what to select
- what to ignore
- how to frame the situation
- when to continue
- when to stop
- when to replan
- what values should shape action

This architecture makes those hidden control decisions explicit.

---

## Non-Goals

This stack does not attempt to be:

- a full AGI architecture
- a production robotics controller
- an LLM agent framework
- a replacement for planning, memory, or perception systems

It is a conceptual and executable study of cognitive control primitives.
