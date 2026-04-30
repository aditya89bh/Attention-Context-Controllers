# Glossary

A short glossary for the Attention & Context Controllers repo.

---

## Attention

The selection mechanism that decides what deserves limited reasoning effort.

In this repo, attention is not transformer attention. It is an agent-level control primitive for deciding which signals should influence behavior.

---

## Context

The frame that gives information meaning.

Context is not just the size of a prompt window. It includes task state, temporal state, environment, goals, constraints, and user/operator intent.

---

## Context Frame

A compact description of the situation the agent is currently in.

Example:

```text
Recovery mode after failed pickup during CNC loading.
```

---

## Salience

A measure of how much a signal or memory matters for the current goal.

In this repo, salience is treated as a weighted combination of relevance, urgency, risk, recency, and goal fit.

---

## Memory

Stored information from previous events, tasks, failures, preferences, or observations.

Memory is useful only when filtered by attention and salience.

---

## Cognitive Budget

The finite amount of reasoning effort an agent can allocate across concerns.

A useful agent should not reason equally about safety, recovery, logging, and background noise.

---

## Temporal Context

The separation of past recall, present execution, and future simulation.

This prevents the agent from confusing what happened, what is happening, and what might happen next.

---

## Interrupt

An incoming signal that may require the agent to pause or switch away from its current task.

Example: force sensor spike during a robot recovery plan.

---

## Goal Arbitration

The process of choosing one active goal when multiple goals compete.

Example:

```text
continue CNC loading
recover failed pickup
answer operator
inspect force anomaly
```

A6 chooses the active goal.

---

## Constraint

A rule or invariant that checks whether a proposed action is allowed.

Constraints may be hard, soft, or audit-only.

---

## Self-Monitoring

A meta-cognitive loop that detects whether the agent is looping, thrashing, repeatedly failing, or drifting.

---

## Long-Horizon Planning

The ability to generate, select, commit to, abandon, and replan multi-step action sequences.

---

## Commitment

The persistence mechanism that prevents an agent from abandoning a plan too easily.

Commitment must be balanced with abandonment logic, otherwise the agent either thrashes or stubbornly repeats bad plans.

---

## Identity

A persistent profile that describes the agent's long-term behavioral orientation.

Example:

```text
Industrial robot that prioritizes safety, accuracy, and transparent recovery behavior.
```

---

## Values

Stable preferences that bias decisions.

Examples:

- safety
- accuracy
- transparency
- efficiency
- resource use

---

## Cognitive Control

The broader control layer that decides what to attend to, what to ignore, what to retrieve, when to switch, when to stay committed, and how to act consistently.
