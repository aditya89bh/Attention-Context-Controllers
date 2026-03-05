"""A9: Long-horizon planning & commitment controller.

Public surface area:
- core data structures (types)
- goal decomposition tree (goal_tree)
- deterministic plan simulator (simulator)
- deterministic planner + commitment controller (planner)

This package is dependency-free and designed for easy iteration.
"""

from .types import (
    Action,
    Goal,
    Plan,
    PlannerConfig,
    PlanStatus,
    PlanStep,
    SimResult,
)
from .goal_tree import GoalNode, GoalTree
from .simulator import PlanSimulator
from .planner import LongHorizonPlanner

__all__ = [
    "Action",
    "Goal",
    "Plan",
    "PlanStep",
    "PlanStatus",
    "PlannerConfig",
    "SimResult",
    "GoalNode",
    "GoalTree",
    "PlanSimulator",
    "LongHorizonPlanner",
]
