# A1 — Context Framing Controller

## What it is

Context Framing converts raw signals into a structured task frame.

It answers:

```text
What situation is the agent in right now?
```

## Why it matters

Without context framing, an agent may reason over raw signals without knowing the operating frame. The same signal can mean different things depending on whether the agent is planning, recovering, executing, explaining, or waiting.

## Failure mode without it

The agent treats all incoming information as flat input and loses the frame of the task.

Example:

```text
Robot failed pickup.
Operator asks for status.
Old memory says tray drifted yesterday.
```

Without context framing, these are just three signals.

With context framing, they become:

```text
Recovery mode after failed pickup during CNC loading.
```

## Input

- raw signals
- current task
- memory hints
- environmental state
- user/operator messages

## Output

A compact task frame.

Example:

```text
Recovery mode after failed pickup during CNC loading.
```

## Tiny demo

Planned file:

```bash
python a1_context_framing/demo_context_framing.py
```

## Robotics connection

A robot needs to know whether it is in normal execution, recovery, inspection, safety override, or operator communication mode. Context framing gives the robot the operating frame before attention, memory retrieval, and planning happen.
