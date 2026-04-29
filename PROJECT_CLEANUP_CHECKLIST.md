# Attention & Context Controllers: Temporary Project Cleanup Checklist

This is a temporary execution checklist for polishing the repository into a complete research-practice artifact.

Delete this file once the cleanup sprint is complete.

---

## Final Definition of Done

The repo is complete when it becomes:

> A polished research-practice repo explaining A1-A10 cognitive control primitives through notes, mini demos, one integrated example, and one final technical blog.

This is not a product, not a production framework, and not a startup rabbit hole.

---

## Phase 1: Repo Reframe and Cleanup

- [ ] Reframe top-level README as a research-practice lab
- [ ] Add clear project goal: understand attention, context, salience, and cognitive control
- [ ] Add explicit note: not a production framework
- [ ] Add completion status table: implemented / partial / planned
- [ ] Add A1-A10 overview table
- [ ] Add quickstart section
- [ ] Add final blog placeholder section
- [ ] Clean folder names for consistent A1-A10 naming

---

## Phase 2: A1-A10 Controller Structure

- [ ] A1 Context Framing README + demo
- [ ] A2 Attention Budgeting README + demo
- [ ] A3 Salience Memory Access README + demo
- [ ] A4 Temporal Context README + demo
- [ ] A5 Interrupt / Task Switching README + demo
- [ ] A6 Goal Arbitration README + demo
- [ ] Polish existing A7 Constraint Enforcement layer
- [ ] Polish existing A8 Self-Monitoring layer
- [ ] Polish existing A9 Long-Horizon Planning layer
- [ ] Polish existing A10 Identity & Value Stabilization layer

Each layer should follow this simple format:

```text
What it is
Why it matters
Failure mode without it
Input
Output
Tiny demo
Robotics connection
```

---

## Phase 3: Mini Demos

- [ ] `demo_context_framing.py` converts raw signals into a useful task frame
- [ ] `demo_attention_budgeting.py` allocates limited reasoning budget
- [ ] `demo_salience_memory_access.py` retrieves relevant memories and ignores noise
- [ ] `demo_temporal_context.py` separates past, present, and future
- [ ] `demo_interrupt_controller.py` decides when to override current task
- [ ] `demo_goal_arbitration.py` chooses between competing goals
- [ ] `demo_constraint_enforcement.py` blocks unsafe or inconsistent actions
- [ ] `demo_self_monitoring.py` detects drift or low confidence
- [ ] `demo_long_horizon_planning.py` shows plan commitment and replanning
- [ ] `demo_identity_value_stabilization.py` biases decisions using values

Minimum acceptable version:

- A1-A6 demos
- Polished A7-A10 existing work

---

## Phase 4: Integrated Cognitive Loop Demo

- [ ] Create `examples/full_cognitive_control_loop.py`
- [ ] Use robotics scenario: CNC loading or failed pickup
- [ ] Show all controller outputs from A1 to A10
- [ ] Keep it deterministic
- [ ] Avoid LLM APIs and external dependencies
- [ ] Make terminal output readable in 30 seconds

Expected demo flow:

```text
Scenario: CNC robot failed pickup

A1 Context Frame:
Recovery mode

A2 Attention Budget:
Failure recovery: 60
Operator communication: 20
Logging: 20

A3 Retrieved Memory:
Tray drift episode

A4 Temporal Context:
Past: tray drift
Present: failed pickup
Future: retry with offset

A5 Interrupt:
Force spike overrides current task

A6 Goal:
Recover safe pickup

A7 Constraint:
Reduce speed and avoid collision zone

A8 Self-Monitoring:
Confidence decreased

A9 Plan:
Inspect tray -> adjust offset -> retry pickup -> verify grasp

A10 Value Bias:
Safety over speed
```

---

## Phase 5: Documentation Polish

- [ ] Add `docs/architecture.md`
- [ ] Add `docs/roadmap.md`
- [ ] Add `docs/glossary.md`
- [ ] Add `use_cases/robotics_attention_context.md`
- [ ] Add `use_cases/ai_agent_assistant.md`
- [ ] Add `use_cases/founder_call_copilot.md`

---

## Phase 6: Tests and Quickstart

- [ ] Add simple tests for A1-A3
- [ ] Add simple tests for A9-A10
- [ ] Add `requirements.txt` or `pyproject.toml`
- [ ] Add quickstart command: `python examples/full_cognitive_control_loop.py`
- [ ] Run all demos once
- [ ] Add final repo status badge/table

Tests are useful, but they should not slow the sprint. Basic smoke tests are enough.

---

## Phase 7: Final Blog

- [ ] Choose final blog title
- [ ] Write blog outline
- [ ] Add repo screenshots or terminal output
- [ ] Explain A1-A10 stack
- [ ] Add robotics example
- [ ] Publish on Substack
- [ ] Cross-post on Medium
- [ ] Share short LinkedIn/X version

Suggested title:

> Memory Is Not Attention: Building a Cognitive Control Layer for AI Agents

---

## 5-Day Timeline

### Day 1: Clean the Skeleton

- [ ] Rewrite top-level README
- [ ] Normalize folder names
- [ ] Add A1-A10 overview table
- [ ] Add `docs/architecture.md`
- [ ] Add `docs/roadmap.md`

Target: 50% complete

### Day 2: A1-A3 Core Attention Stack

- [ ] A1 Context Framing README
- [ ] A1 demo
- [ ] A2 Attention Budgeting README
- [ ] A2 demo
- [ ] A3 Salience Memory Access README
- [ ] A3 demo

Target: 65% complete

### Day 3: A4-A6 Control Stack

- [ ] A4 Temporal Context README
- [ ] A4 demo
- [ ] A5 Interrupt Controller README
- [ ] A5 demo
- [ ] A6 Goal Arbitration README
- [ ] A6 demo

Target: 75% complete

### Day 4: Polish A7-A10 + Integrated Demo

- [ ] Polish A7 README
- [ ] Polish A8 README
- [ ] Polish A9 README
- [ ] Polish A10 README
- [ ] Create full A1-A10 demo
- [ ] Add robotics use case

Target: 85% complete

### Day 5: Final Polish + Blog Draft

- [ ] Add quickstart
- [ ] Add tests or smoke checks
- [ ] Run all demos
- [ ] Add final completion status
- [ ] Draft technical blog
- [ ] Prepare Substack/Medium version

Target: 90% complete

---

## 3-Day Fast Version

### Day 1

- [ ] README rewrite
- [ ] A1-A10 status table
- [ ] Folder cleanup
- [ ] Architecture doc

### Day 2

- [ ] A1-A6 README notes
- [ ] A1-A3 demos
- [ ] A4-A6 demos if time allows

### Day 3

- [ ] Polish A7-A10
- [ ] Full integrated demo
- [ ] Robotics use case
- [ ] Blog outline

Target: 80-85% complete

---

## Strict Scope Rules

- [ ] No productization
- [ ] No UI
- [ ] No LLM API
- [ ] No huge framework
- [ ] No 30-day research rabbit hole
- [ ] One README + one demo per layer
- [ ] One final blog
- [ ] Stop at 85-90%

---

## First Cleaning Commands

```bash
git checkout -b polish/a1-a10-study-lab
find . -maxdepth 2 -type f | sort
```

Then clean the README and folder structure first.
