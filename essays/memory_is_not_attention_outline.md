# Memory Is Not Attention: Building a Cognitive Control Layer for AI Agents

This is the working outline for the final Substack / Medium technical blog.

---

## 1. Opening

I started this project with a simple question:

```text
If memory tells an AI agent what it knows, what tells it what matters?
```

Most agent systems today are obsessed with memory, tools, and longer context windows. But long-horizon failures often come from poor control over attention.

---

## 2. The Problem

Agents often:

- retrieve too much
- reason over irrelevant signals
- confuse memory with current state
- overreact to interruptions
- drift away from the goal
- keep repeating failed actions

The issue is not always lack of information. Often, the issue is lack of control.

---

## 3. Core Distinction

```text
Memory stores.
Attention selects.
Context frames.
Planning sequences.
Values bias action.
Self-monitoring corrects drift.
```

This distinction became the foundation of the repo.

---

## 4. The A1-A10 Stack

Briefly explain each layer:

- A1 Context Framing
- A2 Attention Budgeting
- A3 Salience Memory Access
- A4 Temporal Context
- A5 Interrupt / Task Switching
- A6 Goal Arbitration
- A7 Constraint Enforcement
- A8 Self-Monitoring
- A9 Long-Horizon Planning
- A10 Identity & Value Stabilization

---

## 5. Robotics Example

Use the CNC failed-pickup scenario:

```text
failed pickup -> tray drift memory -> recovery context -> safer retry plan
```

Explain why attention matters more in physical agents:

```text
For chat agents, poor attention creates bad answers.
For robots, poor attention creates bad actions.
```

---

## 6. What I Built

Explain the repo as a research-practice artifact:

- A1-A10 notes
- deterministic mini demos
- full cognitive control loop demo
- robotics use case
- no LLM API
- no product claim

---

## 7. What I Learned

Key lessons:

- Longer context is not the same as better context.
- Memory without salience becomes noise.
- Agents need interruption logic, not just task lists.
- Planning needs commitment and abandonment.
- Values should bias action explicitly.

---

## 8. Why This Matters for Agent Design

The future of agent design may not just be larger models or longer context windows.

It may require explicit cognitive control layers that decide:

- what to attend to
- what to ignore
- what to retrieve
- when to switch
- when to stay committed
- when to replan

---

## 9. Closing

The final takeaway:

```text
The next step for agents is not just more memory.
It is better attention over memory.
```

---

## Possible LinkedIn Hook

Memory is not attention.

Most AI agent systems are adding memory, tools, and longer context windows.

But in long-horizon tasks, the deeper failure is often focus.

The agent remembers too much, retrieves the wrong thing, reacts to noise, and drifts away from the goal.

So I built a small research-practice repo around one question:

What if agents had an explicit cognitive control layer?
