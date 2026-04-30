# A4 — Temporal Context Controller

## What it is

Temporal Context separates past recall, present execution, and future simulation.

It answers:

```text
Is this information about the past, present, or possible future?
```

## Why it matters

Agents often mix memory, current state, and imagined outcomes into one messy context. Temporal separation helps prevent confusion between what happened, what is happening, and what might happen next.

## Failure mode without it

The agent treats remembered events, current observations, and simulated possibilities as equally real.

Example:

```text
Past: tray drift happened yesterday
Present: pickup failed now
Future: retry may work with offset
```

Without temporal context, the agent may confuse a future hypothesis with a current fact.

## Input

- retrieved memories
- current observations
- candidate plans
- predicted outcomes

## Output

A temporal frame.

Example:

```text
Past: tray drift episode
Present: failed pickup
Future: retry with adjusted offset
```

## Tiny demo

Planned file:

```bash
python a4_temporal_context/demo_temporal_context.py
```

## Robotics connection

Robots operate through time. They need to distinguish previous failures, current sensor state, and future recovery actions before executing physical movement.
