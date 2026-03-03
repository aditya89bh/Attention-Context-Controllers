# A8 — Self-Monitoring & Introspection Controller

A8 is a deterministic meta-cognitive control layer that monitors an agent’s recent behavior and emits introspection signals when behavior becomes unstable, repetitive, or invariant-blocked.

A8 does not train models and does not inspect LLM internals. It operates purely on behavior traces (event logs) and produces structured issues and suggested interventions.

Architectural Position

A1 Context Framing  
A2 Attention Budgeting  
A3 Salience Memory Access  
A4 Temporal Context  
A5 Task Switching  
A6 Goal Arbitration  
A7 Consistency & Constraint Enforcement  
A8 Self-Monitoring & Introspection ← Current Layer  
A9 Long-Horizon Planning & Commitment  
A10 Identity & Value Stabilization  

Primitive Introduced

Meta-cognitive feedback loop.

A7 enforces “is this allowed and coherent?”  
A8 enforces “is this working, or am I spiraling?”

Without A8:
- agents loop on repeated actions
- agents thrash between tasks without progress
- agents repeatedly hit the same constraint wall
- agents waste cycles on unstable behavior

What A8 Consumes

A8 consumes an event stream (list of dicts). Typically this is A7’s WorldState.history, where events include:
- proposal_accepted
- proposal_blocked (with constraint results and penalties)
- commitment_added / commitment_retracted
A8 can work with any log format as long as events can be normalized into stable signatures.

What A8 Produces

A8 returns an IntrospectionReport containing:
- issues: detected problems (LOOP, THRASH, REPEATED_VIOLATION)
- interventions: suggested corrective actions (pause_and_replan, stabilize_focus, escalate_or_adjust)
- notes: metadata (window size, events analyzed)

Core Detectors

1. Loop Detector
Detects repeated identical signatures within a sliding window.
Example: action:search repeated 6 times.

2. Thrash Detector
Detects excessive switching between different signatures.
Example: action:plan → action:search → action:plan → action:search.

3. Repeated Violation Detector
Detects repeated blocking by the same constraint_id from A7-style blocked events.
Example: require_human_for_irreversible triggered 4 times.

Integration with A7

A7 produces the exact kind of trace A8 is designed to monitor.

Typical wiring:

- A7 validates proposals and logs results to world.history
- A8 analyzes world.history and emits issues/interventions
- A6 or the execution loop uses those interventions to adapt behavior

Example (conceptual):

report = a8.analyze(world.history)
if report has LOOP:
  pause and replan
if report has REPEATED_VIOLATION:
  request missing approvals or change strategy
if report has THRASH:
  lock a goal/task for a short horizon

Project Structure

a8/
  __init__.py
  types.py
  detectors.py
  controller.py

demo/
  __init__.py
  demo_looping.py
  demo_thrashing.py
  demo_repeat_violation.py

Running Demos

From inside project folder:

python -m demo.demo_looping  
python -m demo.demo_thrashing  
python -m demo.demo_repeat_violation  

Open Source Notes

This project is designed as a reusable control-layer primitive. It is modular, deterministic, and compatible with any agent stack that can produce structured behavior logs.

License

MIT
