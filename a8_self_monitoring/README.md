# A8 — Self-Monitoring Controller

## What it is

Self-Monitoring watches an agent's recent behavior and detects instability, repetition, drift, or repeated constraint failures.

It answers:

```text
Is the agent working, or is it spiraling?
```

## Why it matters

Agents can look busy while making no progress. They may loop, thrash between tasks, repeatedly violate constraints, or continue with low confidence.

A8 introduces a meta-cognitive feedback loop: the agent monitors its own behavior trace and emits corrective signals.

## Failure mode without it

The agent may:

- repeat the same failed action
- switch between tasks without progress
- keep hitting the same constraint wall
- continue acting despite low confidence
- waste cycles on unstable behavior

## Input

- behavior events
- accepted proposals
- blocked proposals
- commitment changes
- constraint violations
- recent action history

## Output

An introspection report.

Example:

```text
Issue: LOOP
Severity: HIGH
Intervention: pause_and_replan
Reason: same action repeated 6 times
```

## Existing implementation notes

This layer uses deterministic detectors over behavior traces:

- loop detector
- thrash detector
- repeated violation detector

It does not inspect model internals and does not require ML training.

## Tiny demo

Planned normalized demo file:

```bash
python a8_self_monitoring/demo_self_monitoring.py
```

## Robotics connection

A robot should notice when it is repeatedly failing the same pickup, thrashing between recovery strategies, or repeatedly violating safety constraints. A8 allows the robot to pause, reframe, request help, or replan.
