# A7 — Consistency & Constraint Enforcement Controller

A7 is a deterministic cognitive control layer responsible for enforcing logical coherence, policy constraints, and commitment consistency inside a layered AI agent architecture.

It sits after goal arbitration (A6) and before execution. A6 decides what the agent wants to do. A7 decides whether it is allowed to do it.

This module performs no learning and does not depend on LLM internals. It is pure system design focused on invariant enforcement.

Architecture Position

A1 Context Framing  
A2 Attention Budgeting  
A3 Salience Memory Access  
A4 Temporal Context  
A5 Task Switching  
A6 Goal Arbitration  
A7 Consistency & Constraint Enforcement ← Current Layer  
A8 Self Monitoring (next)

Purpose

A7 introduces the primitive: Logical Coherence Enforcement.

It ensures:
- Actions do not violate global constraints
- Decisions do not contradict active commitments
- Irreversible operations require explicit approval
- Goal changes are monitored for drift
- Violations produce structured penalties for upstream arbitration

Core Concepts

DecisionProposal  
Represents what the agent intends to do next.

Example:
DecisionProposal(
    decision_id="p1",
    decision_type=DecisionType.ACTION,
    payload={"action": "delete_file"},
    tags={"irreversible"}
)

Constraint  
A named invariant that evaluates a proposal against the world state using a predicate function.

Constraints can be:
- HARD (blocking in STRICT mode)
- SOFT (penalty-based warning)

WorldState  
Minimal state required for enforcement:
- facts (external flags such as human approval)
- commitments (active promises)
- history (log of accepted/blocked proposals)

ValidationReport  
Structured result returned by A7:
- allowed (bool)
- constraint evaluation results
- penalties (numeric)
- metadata notes

Enforcement Modes

STRICT  
HARD violations block execution.  
SOFT violations allow execution but add penalties.

SOFT  
HARD violations allow but apply heavy penalties.

AUDIT  
Never blocks. Only reports violations.

Built-in Constraints

1. Irreversible Action Gate  
Requires world.facts["human_approved"] == True when proposal is tagged "irreversible".

2. Commitment Contradiction  
Blocks actions that contradict active commitments.

3. Goal Drift Prevention (SOFT)  
Penalizes changing a committed goal unless explicitly allowed.

Control Flow

proposal → A6 scoring  
proposal → A7.validate(proposal, world)  
if report.allowed:
    execute(proposal)
else:
    re-arbitrate using report.penalties

A7 does not execute actions. It only validates and reports.

Project Structure

a7/
  types.py
  rules.py
  controller.py

demo/
  demo_basic.py
  demo_commitments.py
  demo_goal_drift.py

Running Demos

From inside project folder:

python -m demo.demo_basic  
python -m demo.demo_commitments  
python -m demo.demo_goal_drift  

Each demo proves a distinct enforcement behavior.

Why This Layer Exists

Strategic reasoning must be separated from constraint enforcement. Without A7:
- Goal arbitration can override safety.
- Commitments can drift.
- Agents can repeatedly violate policies.
- Safety becomes entangled with scoring logic.

A7 provides a deterministic invariant boundary between intention and execution.

Future Layers

A8 — Self Monitoring & Introspection  
A9 — Long Horizon Commitment Enforcement  
A10 — Identity & Value Stabilization

License

MIT
