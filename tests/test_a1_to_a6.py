"""Tests for A1-A6 deterministic controller behavior."""

from __future__ import annotations

from attention_context import CognitiveControlLoop, GoalCandidate, MemoryCandidate, Signal


def test_a1_context_framing_recovery_mode() -> None:
    signals = [
        Signal("robot_event", "Failed pickup at tray", urgency=9, risk=7, relevance=10),
        Signal("memory_hint", "Tray drift happened yesterday", urgency=7, risk=6, relevance=9),
    ]
    frame = CognitiveControlLoop.context_framing(signals)
    assert frame["mode"] == "recovery"
    assert "Recovery mode" in frame["summary"]
    assert "check tray pose drift" in frame["focus"]


def test_a2_attention_budget_sums_to_100() -> None:
    budget = CognitiveControlLoop.attention_budgeting(
        {
            "failure_recovery": (10, 9, 8),
            "safety_check": (8, 8, 10),
            "operator_communication": (6, 5, 2),
            "background_logging": (2, 1, 1),
        }
    )
    assert sum(budget.values()) == 100
    assert budget["failure_recovery"] > budget["background_logging"]


def test_a3_salience_selects_relevant_memories() -> None:
    memories = [
        MemoryCandidate("m1", "Tray drift happened yesterday.", 10, 9, 8, 10),
        MemoryCandidate("m2", "Unrelated cafeteria network outage.", 1, 5, 1, 1),
    ]
    selected = CognitiveControlLoop.salience_memory_access(memories)
    selected_ids = [memory.memory_id for memory, _score in selected]
    assert "m1" in selected_ids
    assert "m2" not in selected_ids


def test_a4_temporal_context_has_past_present_future() -> None:
    selected = [(MemoryCandidate("m1", "Tray drift happened yesterday.", 10, 9, 8, 10), 9.0)]
    temporal = CognitiveControlLoop.temporal_context(selected)
    assert temporal["past"]
    assert temporal["present"]
    assert temporal["future"]


def test_a5_interrupt_switches_on_high_risk() -> None:
    decision = CognitiveControlLoop.interrupt_decision(urgency=9, risk=10, relevance=9, commitment=8)
    assert decision["decision"] == "switch_now"


def test_a6_goal_arbitration_selects_best_goal() -> None:
    goals = [
        GoalCandidate("g1", "Continue normal CNC loading", 5, 4, 2, 5),
        GoalCandidate("g2", "Recover failed pickup safely", 10, 9, 9, 9),
    ]
    selected = CognitiveControlLoop.goal_arbitration(goals)
    assert selected.goal_id == "g2"
