# A10 — Identity & Value Stabilization

**One-liner:** A deterministic control layer that maintains a stable agent identity, values, and non‑negotiable constraints over long horizons, while detecting drift and triggering re-stabilization.

---

## Architectural Position

- A1 Context Framing
- A2 Attention Budgeting
- A3 Salience Memory Access
- A4 Temporal Context
- A5 Task Switching
- A6 Goal Arbitration
- A7 Consistency & Constraint Enforcement
- A8 Self‑Monitoring & Introspection
- A9 Long‑Horizon Planning & Commitment
- **A10 Identity & Value Stabilization ← this layer**

---

## Why A10 Exists

Even a well-planned agent can drift:

- tone changes across sessions
- priorities shift without notice
- it violates “non‑negotiables” under pressure
- it becomes inconsistent between similar situations

A10 introduces the primitive:

> **Normative Continuity** — keep identity and values stable, and surface/resolve conflicts explicitly.

---

## What A10 Does (v0)

A10 provides deterministic utilities for:

- **Identity state**: role, audience, tone constraints
- **Values/priorities**: ranked principles that guide trade-offs
- **Policy constraints**: do/don’t rules (non‑negotiables)
- **Drift detection**: compare current behavior against the identity/value/policy profile
- **Stabilization**: generate a deterministic “stabilized prompt block” or constraint summary

No ML training. No model internals. Pure Python control logic.

---

## Project Structure

```
A10_identity_value_stabilization/
  a10/
    __init__.py
    types.py
    identity_store.py
    stabilizer.py
    evaluator.py
  demo/
    demo_identity.py
  tests/
    test_a10.py
  README.md
```

---

## Demo

```bash
python3 A10_identity_value_stabilization/demo/demo_identity.py
```

---

## License

MIT
