"""Demo: long-horizon planning in a tiny grid with a GoalTree.

Run:
  python3 A9_long_horizon_planning/demo/demo_planning.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

# Allow running this script directly from the repo root.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from A9_long_horizon_planning.a9.goal_tree import Goal, GoalTree
from A9_long_horizon_planning.a9.planner import Planner
from A9_long_horizon_planning.a9.simulator import Simulator


State = Tuple[int, int]


@dataclass
class GridDynamics:
    width: int
    height: int
    walls: set[State]

    def actions(self, state: State) -> Iterable[str]:
        return ["U", "D", "L", "R"]

    def step(self, state: State, action: str) -> tuple[State, float]:
        x, y = state
        if action == "U":
            y -= 1
        elif action == "D":
            y += 1
        elif action == "L":
            x -= 1
        elif action == "R":
            x += 1
        nx, ny = x, y
        nx = max(0, min(self.width - 1, nx))
        ny = max(0, min(self.height - 1, ny))
        ns = (nx, ny)
        if ns in self.walls:
            return state, 5.0  # bump cost
        return ns, 1.0


def main():
    dyn = GridDynamics(width=6, height=4, walls={(2, 1), (2, 2), (3, 2)})
    start: State = (0, 0)
    key: State = (5, 0)
    goal: State = (5, 3)

    # GoalTree: (reach key) AND (reach goal)
    gt = GoalTree(
        root=Goal.AND(
            "get-key-then-exit",
            [
                Goal.leaf("reach-key", lambda s: s == key),
                Goal.leaf("reach-exit", lambda s: s == goal),
            ],
        )
    )

    planner = Planner(dynamics=dyn)
    sim = Simulator(dynamics=dyn)

    # Since our GoalTree AND is not temporally-ordered by itself, we do staged planning:
    p1 = planner.plan_to_goal(start, lambda s: s == key)
    if not p1:
        raise SystemExit("No plan to key")

    p2 = planner.plan_to_goal(key, lambda s: s == goal)
    if not p2:
        raise SystemExit("No plan to goal")

    actions = list(p1.actions) + list(p2.actions)
    traj = sim.rollout(start, actions)
    end_state = traj[-1].next_state if traj else start

    print("Start:", start)
    print("Key:", key)
    print("Goal:", goal)
    print("Actions:", "".join(actions))
    print("Total steps:", len(actions))
    print("End:", end_state)
    visited = [start] + [t.next_state for t in traj]
    reached_key = key in visited
    reached_goal = goal in visited
    print("Reached key at any time?", reached_key)
    print("Reached goal at any time?", reached_goal)
    print("GoalTree satisfied (final state)?", gt.satisfied(end_state))
    print("Note: this GoalTree is non-temporal; AND checks the *same* state.")


if __name__ == "__main__":
    main()
