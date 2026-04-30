# A2 — Attention Budgeting Controller

## What it is

Attention Budgeting allocates limited reasoning effort across competing signals, goals, risks, and tasks.

It answers:

```text
How much cognitive effort should each concern receive?
```

## Why it matters

Agents cannot reason deeply about everything all the time. They need a finite cognitive budget, otherwise they overthink low-priority signals and underfocus on urgent ones.

## Failure mode without it

The agent spends equal effort on unequal concerns.

Example:

```text
Robot failed pickup.
Operator asks for status.
Background log arrives.
```

Without budgeting, the agent may waste reasoning on the background log.

With budgeting:

```text
Failure recovery: 60
Operator communication: 25
Logging: 15
```

## Input

- context frame
- active goals
- urgency scores
- risk levels
- available reasoning budget

## Output

A budget allocation across concerns.

Example:

```text
Failure recovery: 60
Operator communication: 25
Logging: 15
```

## Tiny demo

Planned file:

```bash
python a2_attention_budgeting/demo_attention_budgeting.py
```

## Robotics connection

A robot should spend more attention on safety, failure recovery, and task execution than on low-priority logs. Attention budgeting helps prevent bad focus from becoming bad action.
