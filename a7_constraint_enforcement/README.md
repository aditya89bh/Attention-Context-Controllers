# A7 — Constraint Enforcement Controller

## What it is

Constraint Enforcement checks whether a proposed decision or action is allowed before execution.

It answers:

```text
Is this action safe, valid, and consistent with current commitments?
```

A6 decides what the agent wants to do. A7 decides whether the agent is allowed to do it.

## Why it matters

Strategic reasoning should be separated from constraint enforcement. Without this layer, an agent may choose actions that violate safety rules, commitments, or invariants.

## Failure mode without it

The agent may:

- override safety because a goal score is high
- contradict active commitments
- take irreversible action without approval
- drift away from constraints during execution

## Input

- decision proposal
- world state
- active commitments
- hard constraints
- soft constraints
- enforcement mode

## Output

A validation report.

Example:

```text
Allowed: false
Reason: irreversible action requires human approval
Penalty: 10
```

## Existing implementation notes

This layer currently includes a deterministic controller and built-in constraint rules.

Core ideas:

- HARD constraints can block execution
- SOFT constraints can apply penalties
- AUDIT mode can report violations without blocking
- Validation reports can be sent back to upstream arbitration

## Tiny demo

Planned normalized demo file:

```bash
python a7_constraint_enforcement/demo_constraint_enforcement.py
```

## Robotics connection

Before a robot retries a failed action, A7 can check whether the retry violates safety, speed, collision, human approval, or commitment constraints. This prevents bad planning from becoming bad physical action.
