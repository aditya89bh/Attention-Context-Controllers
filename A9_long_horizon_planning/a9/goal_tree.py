"""A9 goal decomposition tree.

This module manages a simple deterministic goal hierarchy used by the A9 planning
layer. It contains **no planning logic**: only goal structure, lookup, and state
(completed flags).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .types import Goal


@dataclass
class GoalNode:
    """A node in the goal decomposition tree."""

    goal: Goal
    children: list["GoalNode"] = field(default_factory=list)
    completed: bool = False


class GoalTree:
    """A deterministic tree that decomposes a root goal into subgoals."""

    def __init__(self, root: Goal):
        """Create a GoalTree with a single root node."""
        self.root = GoalNode(goal=root)

    def find_node(self, goal_id: str) -> Optional[GoalNode]:
        """Return the node with `goal.goal_id == goal_id`, or None if not found."""
        return self._dfs_find(self.root, goal_id)

    def add_subgoal(self, parent_goal_id: str, subgoal: Goal) -> None:
        """Attach `subgoal` as a child under `parent_goal_id`.

        Raises:
            ValueError: if parent_goal_id is not found.
        """
        parent = self.find_node(parent_goal_id)
        if parent is None:
            raise ValueError(f"Parent goal_id not found: {parent_goal_id}")
        parent.children.append(GoalNode(goal=subgoal))

    def mark_completed(self, goal_id: str) -> None:
        """Mark the given goal node as completed.

        Raises:
            ValueError: if goal_id is not found.
        """
        node = self.find_node(goal_id)
        if node is None:
            raise ValueError(f"Goal_id not found: {goal_id}")
        node.completed = True

    def get_open_goals(self) -> list[GoalNode]:
        """Return goals that are currently open to work on.

        Definition (simple + deterministic):

        A node is "open" if:
        - node.completed is False
        - none of its direct children are incomplete (i.e., children do not block)

        This yields a "work the leaves first" behavior.
        """
        open_nodes: list[GoalNode] = []
        for node in self._dfs_nodes(self.root):
            if node.completed:
                continue
            if any((not c.completed) for c in node.children):
                continue
            open_nodes.append(node)
        return open_nodes

    def print_tree(self) -> None:
        """Print the goal hierarchy with indentation and branch characters."""
        lines = self._format_tree(self.root)
        for line in lines:
            print(line)

    # ---- internals ----

    def _dfs_find(self, node: GoalNode, goal_id: str) -> Optional[GoalNode]:
        if node.goal.goal_id == goal_id:
            return node
        for c in node.children:
            found = self._dfs_find(c, goal_id)
            if found is not None:
                return found
        return None

    def _dfs_nodes(self, node: GoalNode) -> list[GoalNode]:
        out = [node]
        for c in node.children:
            out.extend(self._dfs_nodes(c))
        return out

    def _format_tree(self, node: GoalNode) -> list[str]:
        """Return a list of lines for pretty printing."""
        label = f"Goal: {node.goal.description}"
        if node.completed:
            label += " [DONE]"

        if not node.children:
            return [label]

        lines = [label]
        n = len(node.children)
        for i, child in enumerate(node.children):
            is_last = i == n - 1
            branch = "└── " if is_last else "├── "
            child_lines = self._format_tree(child)
            # First line of child
            lines.append(branch + child_lines[0].replace("Goal: ", ""))
            # Remaining lines of child are indented
            pad = "    " if is_last else "│   "
            for rest in child_lines[1:]:
                lines.append(pad + rest.replace("Goal: ", ""))
        return lines
