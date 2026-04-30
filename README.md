# Attention & Context Controllers

_From memory systems to cognitive control_

This repository is a research-practice lab for studying how AI agents decide what matters, what context to carry, what memory to retrieve, and when to stay focused or replan.

It is built around ten cognitive control primitives, A1-A10. Each primitive is meant to be small, explainable, and testable through notes and deterministic mini demos.

This is not a production framework. The goal is to understand the control layer behind reliable long-horizon agents.

---

## Core Thesis

Most agent systems focus on memory, tools, and larger context windows. But long-horizon agents often fail because they do not know what to attend to.

Memory stores information.
Attention selects what matters.
Context frames why it matters.
Planning sequences action.
Values bias decisions.
Self-monitoring corrects drift.

The next step for agents is not just larger memory. It is better attention over memory.

---

## Why This Project Exists

Modern AI agents often:

- retrieve too much information
- reason over low-priority signals
- treat all context equally
- overreact to interruptions
- drift away from the original task
- fail to maintain commitment over time

This repository studies the control primitives needed to reduce those failures.

The focus is conceptual clarity plus runnable mini examples, not productization.

---

## A1-A10 Cognitive Control Stack

| Layer | Controller | Purpose | Current Status |
|---|---|---|---|
| A1 | Context Framing | Convert raw signals into a useful task frame | Planned |
| A2 | Attention Budgeting | Allocate limited reasoning budget across competing concerns | Planned |
| A3 | Salience Memory Access | Retrieve relevant memories and ignore noise | Planned |
| A4 | Temporal Context | Separate past recall, present execution, and future simulation | Planned |
| A5 | Interrupt / Task Switching | Decide when an interruption should override the current task | Planned |
| A6 | Goal Arbitration | Choose between competing goals | Planned |
| A7 | Constraint Enforcement | Block unsafe, inconsistent, or invalid actions | Partial |
| A8 | Self-Monitoring | Detect drift, low confidence, and instability | Partial |
| A9 | Long-Horizon Planning | Generate, commit to, abandon, and replan multi-step plans | Partial |
| A10 | Identity & Value Stabilization | Bias decisions using stable values and identity | Partial |

---

## Core Architecture

```text
Raw Signals
  -> A1 Context Framing
  -> A2 Attention Budgeting
  -> A3 Salience Memory Access
  -> A4 Temporal Context
  -> A5 Interrupt Handling
  -> A6 Goal Arbitration
  -> A7 Constraint Enforcement
  -> A8 Self-Monitoring
  -> A9 Long-Horizon Planning
  -> A10 Identity & Value Stabilization
  -> Action
```

A simple way to read the stack:

- A1 frames the situation.
- A2 decides where reasoning effort goes.
- A3 selects relevant memory.
- A4 separates past, present, and future.
- A5 handles interruptions.
- A6 chooses the active goal.
- A7 checks constraints.
- A8 monitors stability.
- A9 commits to a plan.
- A10 keeps decisions aligned with values.

---

## What This Repository Is

- A study lab for attention, context, salience, and cognitive control
- A collection of small deterministic controller demos
- A technical notebook for agent architecture thinking
- A bridge between cognitive science, AI agents, and robotics
- A foundation for future work in RoboGPT / ekko9-style memory-enabled robots

---

## What This Repository Is Not

- Not a product
- Not a production-ready agent framework
- Not an LLM wrapper
- Not a RAG tuning project
- Not a UI project
- Not a claim that all A1-A10 layers are complete

---

## Planned Final Artifacts

| Artifact | Purpose |
|---|---|
| A1-A10 controller notes | Explain each cognitive primitive clearly |
| A1-A10 mini demos | Make each primitive executable |
| Full cognitive control loop demo | Show the stack working in one robotics scenario |
| Robotics use case | Connect the project to physical AI and RoboGPT |
| Technical blog | Publish the final interpretation on Substack and Medium |

---

## Quickstart

Current quickstart will be finalized during the cleanup sprint.

Target command:

```bash
python examples/full_cognitive_control_loop.py
```

---

## Temporary Cleanup Tracker

The current cleanup sprint is tracked in:

```text
PROJECT_CLEANUP_CHECKLIST.md
```

This file is temporary and should be deleted once the project is complete.

---

## Final Blog Direction

Working title:

> Memory Is Not Attention: Building a Cognitive Control Layer for AI Agents

Core argument:

> A useful agent does not only need to remember. It needs to know what to attend to, what to ignore, what context to carry forward, when to interrupt itself, when to stay committed, and when to replan.

---

## Design Principles

1. Attention is scarce.
2. Context is dynamic.
3. Memory must be filtered.
4. Cognition must degrade gracefully.
5. Interruptions must be first-class events.
6. Long-horizon agents need commitment and replanning.
7. Physical agents need attention even more than chat agents because bad focus becomes bad action.

---

## Status

This repository is currently being polished into a complete research-practice artifact.

Target completion:

- 80-85% complete after the fast 3-day cleanup
- 85-90% complete after the full 5-day cleanup

Completion means portfolio-complete and learning-complete, not production-complete.
