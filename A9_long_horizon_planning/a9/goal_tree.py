"""Goal trees for long-horizon planning.

A GoalTree encodes a hierarchy of goals/sub-goals.

This is useful when:
- you want interpretable intermediate milestones
- you want to plan/solve progressively (e.g., reach subgoal A then B)

This implementation is minimal: AND/OR composition + leaf predicates.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from .types import GoalPredicate, State


@dataclass(frozen=True)
class Goal:
    """A goal node. Either:

    - leaf: predicate is set
    - composite AND/OR: children set + op
    """

    name: str
    predicate: Optional[GoalPredicate] = None
    op: Optional[str] = None  # "AND" | "OR"
    children: tuple["Goal", ...] = ()

    def is_leaf(self) -> bool:
        return self.predicate is not None

    def satisfied(self, state: State) -> bool:
        if self.is_leaf():
            assert self.predicate is not None
            return bool(self.predicate(state))

        if self.op == "AND":
            return all(c.satisfied(state) for c in self.children)
        if self.op == "OR":
            return any(c.satisfied(state) for c in self.children)

        raise ValueError(f"Invalid goal node: {self.name} (op={self.op})")

    @staticmethod
    def leaf(name: str, predicate: GoalPredicate) -> "Goal":
        return Goal(name=name, predicate=predicate)

    @staticmethod
    def AND(name: str, children: Iterable["Goal"]) -> "Goal":
        return Goal(name=name, op="AND", children=tuple(children))

    @staticmethod
    def OR(name: str, children: Iterable["Goal"]) -> "Goal":
        return Goal(name=name, op="OR", children=tuple(children))


@dataclass(frozen=True)
class GoalTree:
    root: Goal

    def satisfied(self, state: State) -> bool:
        return self.root.satisfied(state)
