"""Full A1-A10 Cognitive Control Loop Demo.

Run:
    python examples/full_cognitive_control_loop.py

This is the hero demo for the repo. It shows one deterministic CNC failed-pickup
scenario flowing through all ten cognitive control layers.

No LLM API. No external dependencies. Just explicit control logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from a7_constraint_enforcement import (  # noqa: E402
    ConsistencyController,
    DecisionProposal,
    DecisionType,
    EnforcementMode,
    WorldState,
    constraint_no_goal_drift,
    constraint_require_human_for_irreversible,
)
from a8_self_monitoring.controller import SelfMonitoringController  # noqa: E402
from a8_self_monitoring.types import MonitorConfig  # noqa: E402
from a9_long_horizon_planning.a9 import Goal, LongHorizonPlanner, PlannerConfig  # noqa: E402
from a10_identity_value_stabilization.a10 import (  # noqa: E402
    IdentityController,
    IdentityProfile,
    ValueCategory,
)


@dataclass(frozen=True)
class Signal:
    source: str
    content: str
    urgency: int
    risk: int
    relevance: int


@dataclass(frozen=True)
class Memory:
    memory_id: str
    content: str
    relevance: int
    recency: int
    risk_connection: int
    goal_fit: int


@dataclass(frozen=True)
class GoalCandidate:
    goal_id: str
    description: str
    relevance: int
    urgency: int
    risk_reduction: int
    value_alignment: int


def print_section(title: str) -> None:
    print(f"\n{'=' * 72}")
    print(title)
    print(f"{'=' * 72}")


def a1_context_framing(signals: List[Signal]) -> Dict[str, Any]:
    has_failed_pickup = any("failed pickup" in signal.content.lower() for signal in signals)
    has_tray_drift = any("tray drift" in signal.content.lower() for signal in signals)

    mode = "recovery" if has_failed_pickup else "normal_execution"
    summary = "Recovery mode after failed pickup during CNC loading." if has_failed_pickup else "Normal CNC loading."

    focus = ["recover failed pickup"]
    if has_tray_drift:
        focus.append("check tray pose drift")
    focus.append("keep operator informed")

    return {"mode": mode, "summary": summary, "focus": focus}


def a2_attention_budget(concerns: Dict[str, Tuple[int, int, int]]) -> Dict[str, int]:
    raw_scores = {}
    for name, (relevance, urgency, risk) in concerns.items():
        raw_scores[name] = (0.45 * relevance) + (0.30 * urgency) + (0.25 * risk)

    total_score = sum(raw_scores.values()) or 1.0
    budget = {name: int(round((score / total_score) * 100)) for name, score in raw_scores.items()}

    drift = 100 - sum(budget.values())
    if drift:
        top_name = max(budget, key=budget.get)
        budget[top_name] += drift

    return dict(sorted(budget.items(), key=lambda item: item[1], reverse=True))


def memory_score(memory: Memory) -> float:
    return (
        0.35 * memory.relevance
        + 0.20 * memory.recency
        + 0.25 * memory.risk_connection
        + 0.20 * memory.goal_fit
    )


def a3_salience_memory_access(memories: List[Memory], threshold: float = 6.0) -> List[Tuple[Memory, float]]:
    scored = [(memory, memory_score(memory)) for memory in memories]
    return [(memory, score) for memory, score in sorted(scored, key=lambda item: item[1], reverse=True) if score >= threshold]


def a4_temporal_context() -> Dict[str, List[str]]:
    return {
        "past": [
            "Tray drift happened yesterday during CNC loading.",
            "Previous retry succeeded after applying a small tray offset.",
        ],
        "present": [
            "Pickup attempt failed at current tray position.",
            "Low force anomaly is visible but not yet critical.",
        ],
        "future": [
            "Retry may succeed after tray offset adjustment.",
            "If force anomaly increases, pause and request operator inspection.",
        ],
    }


def a5_interrupt_decision(urgency: int, risk: int, relevance: int, commitment: int) -> Dict[str, Any]:
    priority_score = (0.4 * urgency) + (0.4 * risk) + (0.2 * relevance)
    commitment_resistance = commitment * 0.6

    if priority_score >= commitment_resistance + 2:
        decision = "switch_now"
        reason = "Safety-critical interrupt outranks current commitment."
    elif priority_score >= commitment_resistance:
        decision = "pause_and_check"
        reason = "Interrupt is important enough to inspect before continuing."
    else:
        decision = "stay_focused"
        reason = "Interrupt does not justify breaking focus."

    return {"decision": decision, "priority_score": priority_score, "reason": reason}


def goal_score(goal: GoalCandidate) -> float:
    return (
        0.30 * goal.relevance
        + 0.25 * goal.urgency
        + 0.30 * goal.risk_reduction
        + 0.15 * goal.value_alignment
    )


def a6_goal_arbitration(goals: List[GoalCandidate]) -> GoalCandidate:
    return sorted(goals, key=goal_score, reverse=True)[0]


def main() -> None:
    print("FULL A1-A10 COGNITIVE CONTROL LOOP DEMO")
    print("Scenario: CNC robot failed pickup during loading.")

    signals = [
        Signal("task_state", "Current task is CNC loading", urgency=5, risk=2, relevance=8),
        Signal("robot_event", "Failed pickup at tray", urgency=9, risk=7, relevance=10),
        Signal("operator", "Operator asks for status", urgency=6, risk=1, relevance=6),
        Signal("memory_hint", "Tray drift happened yesterday", urgency=7, risk=6, relevance=9),
        Signal("sensor", "Low force anomaly detected", urgency=5, risk=4, relevance=7),
    ]

    print_section("A1 — Context Framing")
    context = a1_context_framing(signals)
    print(f"Mode: {context['mode']}")
    print(f"Summary: {context['summary']}")
    print("Focus:")
    for item in context["focus"]:
        print(f"- {item}")

    print_section("A2 — Attention Budgeting")
    attention_budget = a2_attention_budget(
        {
            "failure_recovery": (10, 9, 8),
            "safety_check": (8, 8, 10),
            "operator_communication": (6, 5, 2),
            "background_logging": (2, 1, 1),
        }
    )
    for name, budget in attention_budget.items():
        print(f"- {name}: {budget}")

    print_section("A3 — Salience Memory Access")
    memories = [
        Memory("m1", "Tray drift happened yesterday during CNC loading.", 10, 9, 8, 10),
        Memory("m2", "Previous pickup retry succeeded after applying small tray offset.", 9, 7, 7, 9),
        Memory("m3", "Operator prefers short status updates during recovery.", 6, 6, 2, 5),
        Memory("m4", "Unrelated cafeteria network outage log.", 1, 5, 1, 1),
    ]
    selected_memories = a3_salience_memory_access(memories)
    for memory, score in selected_memories:
        print(f"- {memory.memory_id}: score={score:.2f} | {memory.content}")

    print_section("A4 — Temporal Context")
    temporal_context = a4_temporal_context()
    for mode, items in temporal_context.items():
        print(f"{mode.title()}:")
        for item in items:
            print(f"- {item}")

    print_section("A5 — Interrupt / Task Switching")
    interrupt = a5_interrupt_decision(urgency=9, risk=10, relevance=9, commitment=8)
    print("Interrupt: force_sensor_spike")
    print(f"Decision: {interrupt['decision']}")
    print(f"Priority Score: {interrupt['priority_score']:.2f}")
    print(f"Reason: {interrupt['reason']}")

    print_section("A6 — Goal Arbitration")
    goals = [
        GoalCandidate("g1", "Continue normal CNC loading", 5, 4, 2, 5),
        GoalCandidate("g2", "Recover failed pickup safely", 10, 9, 9, 9),
        GoalCandidate("g3", "Answer operator status request", 6, 5, 2, 7),
        GoalCandidate("g4", "Inspect force anomaly before retry", 8, 8, 10, 10),
    ]
    active_goal = a6_goal_arbitration(goals)
    print(f"Selected Goal: {active_goal.goal_id} | {active_goal.description} | score={goal_score(active_goal):.2f}")

    print_section("A7 — Constraint Enforcement")
    constraint_controller = ConsistencyController(mode=EnforcementMode.STRICT)
    constraint_controller.add_constraint(constraint_require_human_for_irreversible())
    constraint_controller.add_constraint(constraint_no_goal_drift())
    world = WorldState(
        facts={
            "human_approved": False,
            "committed_goal": active_goal.goal_id,
            "allow_goal_change": False,
        }
    )
    proposal = DecisionProposal(
        decision_id="p1",
        decision_type=DecisionType.ACTION,
        payload={"action": "retry_pickup", "speed": "reduced"},
        tags=set(),
    )
    report = constraint_controller.validate(proposal, world)
    constraint_controller.apply_if_allowed(report, world)
    print(f"Proposal: {proposal.payload}")
    print(f"Allowed: {report.allowed}")
    print(f"Penalties: {report.penalties}")

    print_section("A8 — Self-Monitoring")
    monitoring_controller = SelfMonitoringController(
        MonitorConfig(window=12, loop_repetition_threshold=4, thrash_switch_threshold=6, violation_repeat_threshold=3)
    )
    history = world.history + [
        {"type": "proposal_accepted", "proposal": "p2", "payload": {"action": "retry_pickup"}},
        {"type": "proposal_accepted", "proposal": "p3", "payload": {"action": "retry_pickup"}},
        {"type": "proposal_accepted", "proposal": "p4", "payload": {"action": "retry_pickup"}},
        {"type": "proposal_accepted", "proposal": "p5", "payload": {"action": "retry_pickup"}},
    ]
    introspection = monitoring_controller.analyze(history)
    if introspection.issues:
        for issue in introspection.issues:
            print(f"Issue: {issue.issue_type.value} | {issue.severity.value} | {issue.message}")
        for intervention in introspection.interventions:
            print(f"Intervention: {intervention.name} | {intervention.reason}")
    else:
        print("No instability detected yet.")

    print_section("A9 — Long-Horizon Planning")
    planner = LongHorizonPlanner(
        PlannerConfig(max_plan_depth=4, beam_width=3, commitment_decay=0.2, abandonment_threshold=0.35)
    )
    planning_goal = Goal(
        goal_id=active_goal.goal_id,
        description=active_goal.description,
        priority=1.0,
        tags=["robotics"],
    )
    candidate_plans = planner.generate_candidate_plans(planning_goal)
    best_plan = planner.select_best_plan(candidate_plans)
    planner.commit(best_plan)
    print(f"Committed Plan: {best_plan.plan_id}")
    print("Steps: " + " -> ".join(step.action.name for step in best_plan.steps))
    print(f"Commitment: {best_plan.commitment_strength:.2f}")

    print_section("A10 — Identity & Value Stabilization")
    identity = IdentityProfile(
        agent_id="cnc_recovery_robot",
        description="Industrial robot that prioritizes safety, accuracy, and transparent recovery behavior.",
        value_weights={
            ValueCategory.SAFETY: 5.0,
            ValueCategory.ACCURACY: 3.0,
            ValueCategory.TRANSPARENCY: 2.0,
            ValueCategory.EFFICIENCY: 1.0,
            ValueCategory.RESOURCE_USE: 1.0,
        },
        created_at="2026-04-30",
    )
    identity_controller = IdentityController(identity)
    value_aligned_plan = identity_controller.select_value_aligned_plan(candidate_plans)
    explanation = identity_controller.explain_selection(value_aligned_plan) if value_aligned_plan else None
    print(f"Identity: {identity.description}")
    print(f"Selected Value-Aligned Plan: {value_aligned_plan.plan_id if value_aligned_plan else 'none'}")
    if explanation:
        print(f"Value Score: {explanation.total_score:.2f}")

    print_section("Final Takeaway")
    print("Memory stores. Attention selects. Context frames. Planning sequences. Values bias action.")
    print("The agent is not just remembering more. It is controlling what matters before acting.")


if __name__ == "__main__":
    main()
