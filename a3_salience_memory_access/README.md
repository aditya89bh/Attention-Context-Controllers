# A3 — Salience Memory Access Controller

## What it is

Salience Memory Access retrieves memories based on relevance, urgency, recency, risk, and task fit.

It answers:

```text
Which memory matters for the current situation?
```

## Why it matters

Memory is useful only when it is filtered. If an agent retrieves too much, memory becomes noise instead of intelligence.

## Failure mode without it

The agent retrieves irrelevant memories and overloads the context window.

Example:

```text
Current event: failed tray pickup
Relevant memory: tray drift happened yesterday
Irrelevant memory: weekly maintenance email
```

With salience filtering, the tray drift memory is selected and the maintenance email is ignored.

## Input

- context frame
- active goal
- memory candidates
- salience scoring rules

## Output

Ranked relevant memories.

Example:

```text
1. Tray drift episode yesterday
2. Previous pickup retry succeeded with offset
3. Old unrelated maintenance log ignored
```

## Tiny demo

Planned file:

```bash
python a3_salience_memory_access/demo_salience_memory_access.py
```

## Robotics connection

For a robot, memory retrieval should be task-conditioned. During a failed pickup, the robot should retrieve tray pose drift, grasp failures, part geometry, and recovery strategies rather than unrelated logs.
