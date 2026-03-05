# A9 — Long Horizon Planning

Minimal, dependency-free scaffolding for experimenting with long-horizon planning concepts:

- simple `GoalTree` (AND/OR + leaf predicates)
- baseline uniform-cost search planner (Dijkstra)
- deterministic simulator for rollouts

This is intentionally small so we can iterate quickly.

## Structure

```
A9_long_horizon_planning/
  a9/
    __init__.py
    types.py
    goal_tree.py
    planner.py
    simulator.py
  demo/
    demo_planning.py
  README.md
```

## Run the demo

From repo root:

```bash
python3 A9_long_horizon_planning/demo/demo_planning.py
```

## Next upgrades (if you want)

- temporal GoalTrees (sequence / options)
- heuristic search (A*)
- stochastic sims + MCTS
- logging + visualization
