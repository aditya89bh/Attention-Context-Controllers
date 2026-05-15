"""End-to-end tests for the CognitiveControlLoop package API."""

from __future__ import annotations

from attention_context import CognitiveControlLoop, GoalCandidate, MemoryCandidate, Signal


def test_full_loop_returns_structured_outputs() -> None:
    signals = [
        Signal("robot_event", "Failed pickup at tray", urgency=9, risk=7, relevance=10),
        Signal("memory_hint", "Tray drift happened yesterday", urgency=7, risk=6, relevance=9),
    ]
    memories = [
        MemoryCandidate("m1", "Tray drift happened yesterday during CNC loading.", 10, 9, 8, 10),
        MemoryCandidate("m2", "Previous pickup retry succeeded after applying small tray offset.", 9, 7, 7, 9),
    ]
    goals = [
        GoalCandidate("g1", "Continue normal CNC loading", 5, 4, 2, 5),
        GoalCandidate("g2", "Recover failed pickup safely", 10, 9, 9, 9),
    ]

    result = CognitiveControlLoop().run(signals=signals, memories=memories, goals=goals)

    assert result.context_frame["mode"] == "recovery"
    assert sum(result.attention_budget.values()) == 100
    assert len(result.selected_memories) >= 1
    assert result.temporal_context["past"]
    assert result.interrupt_decision["decision"] == "switch_now"
    assert result.active_goal.goal_id == "g2"
    assert result.constraint_report.allowed is True
    assert result.self_monitoring_report.issues
    assert result.committed_plan is not None
    assert result.value_aligned_plan is not None
