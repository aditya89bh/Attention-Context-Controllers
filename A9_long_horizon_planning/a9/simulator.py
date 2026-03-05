"""A tiny deterministic simulator.

This is intentionally simple: given Dynamics, roll out a plan.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .types import Action, Dynamics, State, Transition


@dataclass
class Simulator:
    dynamics: Dynamics

    def rollout(self, start: State, actions: Iterable[Action]) -> list[Transition]:
        traj: List[Transition] = []
        s = start
        for a in actions:
            ns, cost = self.dynamics.step(s, a)
            traj.append(Transition(state=s, action=a, next_state=ns, cost=cost))
            s = ns
        return traj
