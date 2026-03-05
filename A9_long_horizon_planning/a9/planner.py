"""Baseline planner for toy long-horizon tasks.

Implements a simple uniform-cost search (Dijkstra) over a discrete state space.

Notes:
- This is a baseline, not a production planner.
- Works well for small deterministic environments.
"""

from __future__ import annotations

from dataclasses import dataclass
import heapq
from typing import Dict, Iterable, List, Optional, Tuple

from .types import Action, Dynamics, State


@dataclass(frozen=True)
class Plan:
    actions: tuple[Action, ...]
    cost: float
    states: tuple[State, ...]


@dataclass
class Planner:
    dynamics: Dynamics
    max_expansions: int = 100_000

    def plan_to_goal(self, start: State, is_goal) -> Optional[Plan]:
        """Uniform-cost search to any state satisfying is_goal(state)->bool."""

        # priority queue items: (cost, state)
        pq: List[Tuple[float, State]] = [(0.0, start)]
        best_cost: Dict[State, float] = {start: 0.0}
        parent: Dict[State, Tuple[State, Action]] = {}

        expansions = 0
        while pq:
            cost, s = heapq.heappop(pq)
            if cost != best_cost.get(s, float("inf")):
                continue

            if is_goal(s):
                return self._reconstruct(start, s, parent, cost)

            expansions += 1
            if expansions > self.max_expansions:
                return None

            for a in self.dynamics.actions(s):
                ns, step_cost = self.dynamics.step(s, a)
                ncost = cost + float(step_cost)
                if ncost < best_cost.get(ns, float("inf")):
                    best_cost[ns] = ncost
                    parent[ns] = (s, a)
                    heapq.heappush(pq, (ncost, ns))

        return None

    def _reconstruct(
        self,
        start: State,
        goal: State,
        parent: Dict[State, Tuple[State, Action]],
        cost: float,
    ) -> Plan:
        actions: List[Action] = []
        states: List[State] = [goal]
        s = goal
        while s != start:
            ps, a = parent[s]
            actions.append(a)
            states.append(ps)
            s = ps
        actions.reverse()
        states.reverse()
        return Plan(actions=tuple(actions), cost=cost, states=tuple(states))
