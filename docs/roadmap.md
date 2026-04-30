# Roadmap: Cleanup Sprint

This roadmap defines the scope required to finish the Attention & Context Controllers repo as a polished research-practice artifact.

The goal is not product completion. The goal is learning completion and portfolio completion.

---

## Final Definition of Done

The project is done when it contains:

- a clear top-level README
- a consistent A1-A10 structure
- one note and one demo per controller layer
- one integrated cognitive control loop demo
- one robotics use case
- one final technical blog draft or outline

---

## Scope Rules

- No productization
- No UI
- No LLM API dependency
- No huge framework
- No 30-day research rabbit hole
- One README plus one demo per layer
- Stop at 85-90% completion

---

## Phase 1: Repo Reframe and Cleanup

Status: In progress

Tasks:

- [x] Reframe README as research-practice lab
- [x] Add A1-A10 overview table
- [x] Add target quickstart section
- [x] Add final blog direction
- [x] Add architecture document
- [ ] Normalize folder structure
- [ ] Add glossary

---

## Phase 2: A1-A3 Core Attention Stack

Status: Planned

Tasks:

- [ ] A1 Context Framing README
- [ ] A1 deterministic demo
- [ ] A2 Attention Budgeting README
- [ ] A2 deterministic demo
- [ ] A3 Salience Memory Access README
- [ ] A3 deterministic demo

These three layers are the core of the project because they directly answer:

```text
What matters right now?
Why does it matter?
Which memory is relevant?
```

---

## Phase 3: A4-A6 Control Stack

Status: Planned

Tasks:

- [ ] A4 Temporal Context README
- [ ] A4 deterministic demo
- [ ] A5 Interrupt / Task Switching README
- [ ] A5 deterministic demo
- [ ] A6 Goal Arbitration README
- [ ] A6 deterministic demo

These layers explain how agents manage time, interruption, and competing goals.

---

## Phase 4: A7-A10 Polish

Status: Partial

Tasks:

- [ ] Polish A7 Constraint Enforcement README
- [ ] Polish A8 Self-Monitoring README
- [ ] Polish A9 Long-Horizon Planning README
- [ ] Polish A10 Identity & Value Stabilization README
- [ ] Ensure each existing layer has a clear demo path

These layers already exist in partial form and should be standardized rather than rebuilt.

---

## Phase 5: Integrated Demo

Status: Planned

Tasks:

- [ ] Create `examples/full_cognitive_control_loop.py`
- [ ] Use CNC failed pickup scenario
- [ ] Print A1-A10 outputs clearly
- [ ] Keep it deterministic
- [ ] Avoid external dependencies

This is the hero demo for the repository.

---

## Phase 6: Use Cases and Blog

Status: Planned

Tasks:

- [ ] Add robotics use case
- [ ] Add AI assistant use case
- [ ] Add founder call copilot use case
- [ ] Draft final technical blog outline

Working blog title:

```text
Memory Is Not Attention: Building a Cognitive Control Layer for AI Agents
```

---

## Target Completion

| Sprint Version | Target Completion |
|---|---:|
| 3-day cleanup | 80-85% |
| 5-day cleanup | 85-90% |

Completion means the repo is learning-complete and portfolio-complete, not production-complete.
