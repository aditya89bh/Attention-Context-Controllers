# Robotics Use Case: Attention and Context in CNC Recovery

This use case connects the A1-A10 cognitive control stack to a physical robotics scenario.

Scenario:

A robot is loading a CNC machine. During pickup, the gripper fails to secure the workpiece. The robot receives multiple signals at once:

- failed pickup event
- tray drift memory from yesterday
- operator status request
- low force anomaly
- current CNC loading task
- unrelated background log

The question is not simply:

```text
What does the robot know?
```

The harder question is:

```text
What should the robot attend to before acting?
```

---

## A1 Context Framing

The robot frames the situation as:

```text
Recovery mode after failed pickup during CNC loading.
```

This prevents it from treating the failed pickup as a random event.

---

## A2 Attention Budgeting

The robot allocates limited reasoning budget:

```text
failure_recovery: high
safety_check: high
operator_communication: medium
background_logging: low
```

This prevents equal reasoning over unequal concerns.

---

## A3 Salience Memory Access

The robot retrieves:

```text
Tray drift happened yesterday.
Previous retry succeeded with small tray offset.
```

It ignores unrelated maintenance logs.

---

## A4 Temporal Context

The robot separates:

```text
Past: tray drift episode
Present: failed pickup and low force anomaly
Future: retry after offset adjustment
```

This prevents memory, observation, and prediction from collapsing into one messy context.

---

## A5 Interrupt / Task Switching

If the force anomaly becomes safety-critical, the robot pauses the recovery plan.

This prevents brittle focus.

---

## A6 Goal Arbitration

Competing goals:

```text
continue CNC loading
recover failed pickup
answer operator
inspect force anomaly
```

Selected goal:

```text
recover failed pickup safely
```

---

## A7 Constraint Enforcement

Before retrying, the robot checks constraints:

- reduced speed during recovery
- collision zone avoidance
- human approval for irreversible actions
- no goal drift unless explicitly allowed

This prevents bad plans from becoming bad physical action.

---

## A8 Self-Monitoring

If the robot retries the same failed action repeatedly, A8 detects a loop and suggests:

```text
pause_and_replan
```

---

## A9 Long-Horizon Planning

The robot commits to a recovery sequence:

```text
inspect tray -> adjust offset -> retry pickup -> verify grasp
```

---

## A10 Identity & Value Stabilization

The robot's operating values bias decisions toward:

```text
safety over speed
accuracy over raw efficiency
transparent recovery over silent failure
```

---

## Why This Matters

For chat agents, poor attention creates bad answers.

For robots, poor attention creates bad actions.

A physical agent cannot afford to reason over every signal equally. It needs a control layer that decides what matters before movement happens.

This is the central design argument of the repository.
