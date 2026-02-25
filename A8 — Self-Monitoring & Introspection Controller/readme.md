# A8 — Self-Monitoring & Introspection Controller

A8 is a deterministic meta-cognitive control layer that monitors an agent’s recent behavior and triggers introspection signals when performance or stability degrades.

A8 does not train models.
A8 does not inspect LLM internals.
A8 observes behavior traces and emits structured self-monitoring alerts.

## Architectural Position

A1 Context Framing  
A2 Attention Budgeting  
A3 Salience Memory Access  
A4 Temporal Context  
A5 Task Switching  
A6 Goal Arbitration  
A7 Consistency & Constraint Enforcement  
A8 Self-Monitoring & Introspection ← Current Layer  
A9 Long-Horizon Planning & Commitment  
A10 Identity & Value Stabilization

## Why A8 Exists (and Why It Follows A7)

A7 enforces “is this allowed and coherent?”
A8 enforces “is this working, or am I spiraling?”

Without A8:
- agents repeat failures without adapting
- agents loop or thrash between tasks
- agents repeatedly hit the same constraint gates
- execution becomes noisy, unstable, and time-wastey

A8 introduces the primitive:
Meta-cognitive feedback loop.

## What A8 Observes

A8 observes an event stream (history), typically logged by A7:
- proposal_accepted
- proposal_blocked
- penalties
- commitment changes
- any relevant metadata you choose to log

A8 is compatible with other logs too, as long as events are normalized.

## What A8 Outputs

A8 returns an IntrospectionReport containing:
- detected issues (looping, thrashing, repeated constraint violations)
- severity scores
- suggested interventions (pause, replan, change strategy, escalate)

## Core Detectors (v1)

1) Loop Detector
Detects repeated identical actions/proposals in a sliding window.

2) Thrash Detector
Detects rapid switching between different actions/goals without progress.

3) Repeated Violation Detector
Detects repeated blocking by the same constraint(s), indicating the agent is pushing against an invariant.

## Demos

- demo_looping.py: repeated identical action triggers LOOP signal
- demo_thrashing.py: alternating actions triggers THRASH signal
- demo_repeat_violation.py: repeated A7 blocks triggers VIOLATION_PATTERN signal

## Repo Structure

a8/
  types.py
  detectors.py
  controller.py

demo/
  demo_looping.py
  demo_thrashing.py
  demo_repeat_violation.py
