# A7 — Consistency & Constraint Enforcement Controller
_Logical coherence enforcement for cognitive-control agents (no ML training)._

A7 ensures the agent’s chosen goals, plan steps, and actions remain **consistent** with:
- global constraints (policies, invariants)
- past commitments (promises, locked goals, “I will not do X”)
- safety gates (approvals for irreversible or sensitive actions)

This project is:
- **Pure Python**
- **Modular**
- **Colab-runnable**
- **GitHub-structured**
- **Focused on agent behavior** (system design, not LLM internals)

---

## Why A7 Exists (and Why It Follows A6)

A6 selects the dominant goal when multiple threads exist.

A7 answers the next question:

> “Even if this goal/action is optimal… is it allowed, coherent, and non-contradictory?”

Without A7:
- the agent can optimize but violate policies
- the agent can contradict its own commitments
- multi-thread execution can drift into inconsistent states
- “fast decisions” become “fast disasters”

---

## Cognitive Control Primitive

**Logical coherence enforcement**

A7 provides a deterministic validation layer that:
1. checks a proposed decision/action against constraints
2. detects contradictions with active commitments
3. returns an enforceable verdict (allow, block, warn + penalize, audit)

Output is a **Validation Report** that downstream layers can use:
- A6 can re-arbitrate with penalties
- A8 can introspect repeated violations or drift
- A9 can lock commitments and checkpoint them

---

## Inputs and Outputs

### Inputs (conceptually from A1–A6)
A7 is designed to consume **simple dictionaries** or dataclasses from earlier layers:

- From **A1 Context Framing**
  - context tags / environment mode (work, safety, deadline, etc.)

- From **A4 Temporal Context**
  - time, deadlines (optional for time-based constraints)

- From **A6 Goal Arbitration**
  - selected goal + directive
  - proposed next action/plan step

- From **A5 Task Switching**
  - thread state (optional: to prevent drift across threads)

### Core A7 Inputs (direct)
- `DecisionProposal` (what the agent is about to do)
- `WorldState` (minimal state needed for invariants)
  - `facts` (flags like human approval, environment conditions)
  - `commitments` (active promises)
  - `history` (past accepted/blocked decisions)

### Outputs
- `ValidationReport`
  - `allowed: bool`
  - `results: List[ConstraintResult]`
  - `penalties: Dict[str, float]` (for soft violations)
  - `notes` (debug + audit metadata)

---

## Core Concepts

### 1) Decision Proposal
Everything is validated as a proposal:
- GOAL_SELECT: `{goal_id: "..."}`
- PLAN_STEP: `{plan_id: "...", step: "..."}`
- ACTION: `{action: "...", args: {...}}`

Proposals also carry tags:
- `irreversible`
- `safety_sensitive`
- `requires_human`
- etc.

### 2) Constraints (Invariants + Policies)
A constraint is a named rule:
- **HARD**: violation blocks (in STRICT mode)
- **SOFT**: violation allows but penalizes (or warns)

Each constraint:
- declares what decision types it applies to
- optionally requires certain tags to apply
- uses a predicate: `(proposal, world_state) -> bool`

### 3) Commitment System
Commitments represent:
- promises (“do not send email until reviewed”)
- locked goals (“stay committed to goal g1”)
- selected policies (“strict safety mode”)

A7 checks:
- does this proposal contradict any active commitment?

### 4) Enforcement Modes
A7 can be run in different modes:
- **STRICT**: HARD violations block, SOFT violations penalize
- **SOFT**: HARD violations do not block but penalize heavily
- **AUDIT**: never block; always report

This lets you run A7 in “debug/audit” first, then tighten it.

---

## Suggested Project Structure
