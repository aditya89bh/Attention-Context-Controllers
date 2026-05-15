"""Reusable CognitiveControlLoop API.

This module turns the repo's deterministic demo logic into a small reusable
package surface.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from a7_constraint_enforcement import (
    ConsistencyController,
    DecisionProposal,
    DecisionType,
    EnforcementMode,
    WorldState,
    constraint_no_goal_drift,
    constraint_require_human_for_irreversible,
)
from a8_self_monitoring.controller import SelfMonitoringController
from a8_self_monitoring.types import MonitorConfig
from a9_long_horizon_planning.a9 import Goal, LongHorizonPlanner, PlannerConfig
from a10_identity_value_stabilization.a10 import (
    IdentityController,
    IdentityProfile,
    ValueCategory,
)

from .types import ControlLoopResult, GoalCandidate, MemoryCandidate, Signal


class CognitiveControlLoop:
    """Small deterministic A1-A10 cognitive control loop."""

    def run(
        self,
        signals: List[Signal],
        memories: List[MemoryCandidate],
        goals: List[GoalCandidate],
    ) -> ControlLoopResult:
        """Run signals, memories, and goals through A1-A10."""
        context_frame = self.context_framing(signals)
        attention_budget = self.attention_budgeting(
            {
                "failure_recovery": (10, 9, 8),
                "safety_check": (8, 8, 10),
                "operator_communication": (6, 5, 2),
                "background_logging": (2, 1, 1),
            }
        )
        selected_memories = self.salience_memory_access(memories)
        temporal_context = self.temporal_context(selected_memories)
        interrupt_decision = self.interrupt_decision(urgency=9, risk=10, relevance=9, commitment=8)
        active_goal = self.goal_arbitration(goals)

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
        constraint_report = constraint_controller.validate(proposal, world)
        constraint_controller.apply_if_allowed(constraint_report, world)

        history = world.history + [
            {"type": "proposal_accepted", "proposal": "p2", "payload": {"action": "retry_pickup"}},
            {"type": "proposal_accepted", "proposal": "p3", "payload": {"action": "retry_pickup"}},
            {"type": "proposal_accepted", "proposal": "p4", "payload": {"action": "retry_pickup"}},
            {"type": "proposal_accepted", "proposal": "p5", "payload": {"action": "retry_pickup"}},
        ]
        self_monitoring_report = SelfMonitoringController(
            MonitorConfig(window=12, loop_repetition_threshold=4, thrash_switch_threshold=6, violation_repeat_threshold=3)
        ).analyze(history)

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
        committed_plan = planner.commit(planner.select_best_plan(candidate_plans))

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
        value_aligned_plan = IdentityController(identity).select_value_aligned_plan(candidate_plans)

        return ControlLoopResult(
            context_frame=context_frame,
            attention_budget=attention_budget,
            selected_memories=selected_memories,
            temporal_context=temporal_context,
            interrupt_decision=interrupt_decision,
            active_goal=active_goal,
            constraint_report=constraint_report,
            self_monitoring_report=self_monitoring_report,
            committed_plan=committed_plan,
            value_aligned_plan=value_aligned_plan,
            notes={"scenario": "CNC failed-pickup recovery"},
        )

    @staticmethod
    def context_framing(signals: List[Signal]) -> Dict[str, Any]:
        has_failed_pickup = any("failed pickup" in signal.content.lower() for signal in signals)
        has_tray_drift = any("tray drift" in signal.content.lower() for signal in signals)
        mode = "recovery" if has_failed_pickup else "normal_execution"
        summary = "Recovery mode after failed pickup during CNC loading." if has_failed_pickup else "Normal CNC loading."
        focus = ["recover failed pickup"] if has_failed_pickup else ["continue task"]
        if has_tray_drift:
            focus.append("check tray pose drift")
        focus.append("keep operator informed")
        return {"mode": mode, "summary": summary, "focus": focus}

    @staticmethod
    def attention_budgeting(concerns: Dict[str, Tuple[int, int, int]]) -> Dict[str, int]:
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

    @staticmethod
    def salience_memory_access(memories: List[MemoryCandidate], threshold: float = 6.0) -> List[Tuple[MemoryCandidate, float]]:
        scored = [(memory, CognitiveControlLoop.memory_score(memory)) for memory in memories]
        return [(memory, score) for memory, score in sorted(scored, key=lambda item: item[1], reverse=True) if score >= threshold]

    @staticmethod
    def memory_score(memory: MemoryCandidate) -> float:
        return (
            0.35 * memory.relevance
            + 0.20 * memory.recency
            + 0.25 * memory.risk_connection
            + 0.20 * memory.goal_fit
        )

    @staticmethod
    def temporal_context(selected_memories: List[Tuple[MemoryCandidate, float]]) -> Dict[str, List[str]]:
        return {
            "past": [memory.content for memory, _score in selected_memories[:2]],
            "present": [
                "Pickup attempt failed at current tray position.",
                "Low force anomaly is visible but not yet critical.",
            ],
            "future": [
                "Retry may succeed after tray offset adjustment.",
                "If force anomaly increases, pause and request operator inspection.",
            ],
        }

    @staticmethod
    def interrupt_decision(urgency: int, risk: int, relevance: int, commitment: int) -> Dict[str, Any]:
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

    @staticmethod
    def goal_arbitration(goals: List[GoalCandidate]) -> GoalCandidate:
        if not goals:
            raise ValueError("CognitiveControlLoop requires at least one goal candidate")
        return sorted(goals, key=CognitiveControlLoop.goal_score, reverse=True)[0]

    @staticmethod
    def goal_score(goal: GoalCandidate) -> float:
        return (
            0.30 * goal.relevance
            + 0.25 * goal.urgency
            + 0.30 * goal.risk_reduction
            + 0.15 * goal.value_alignment
        )
