"""Shared types for planning + simulation.

Design goals:
- Keep it tiny and readable.
- Prefer Protocols over heavy base classes.
- Allow deterministic toy sims for experiments.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Hashable, Iterable, Mapping, Protocol, Sequence, TypeVar


State = Hashable
Action = Hashable


@dataclass(frozen=True)
class Transition:
    """A single step in a trajectory."""

    state: State
    action: Action
    next_state: State
    cost: float = 1.0


class Dynamics(Protocol):
    """Environment dynamics for planning."""

    def actions(self, state: State) -> Iterable[Action]:
        ...

    def step(self, state: State, action: Action) -> tuple[State, float]:
        """Return (next_state, cost)."""
        ...


class GoalPredicate(Protocol):
    def __call__(self, state: State) -> bool: ...


T = TypeVar("T")


def argmin(items: Iterable[T], key: Callable[[T], float]) -> T:
    """Return item with minimal key value."""
    best = None
    best_v = None
    for x in items:
        v = key(x)
        if best is None or v < best_v:  # type: ignore[operator]
            best = x
            best_v = v
    if best is None:
        raise ValueError("argmin() received empty iterable")
    return best
