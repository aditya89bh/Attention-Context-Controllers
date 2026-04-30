"""A9 goal decomposition tree."""

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
        self.root = GoalNode(goal=root)

    def find_node(self, goal_id: str) -> Optional[GoalNode]:
        """Return the node with goal.goal_id == goal_id, or None if not found."""
        return self._dfs_find(self.root, goal_id)

    def add_subgoal(self, parent_goal_id: str, subgoal: Goal) -> None:
        """Attach subgoal as a child under parent_goal_id."""
        parent = self.find_node(parent_goal_id)
        if parent is None:
            raise ValueError(f"Parent goal_id not found: {parent_goal_id}")
        parent.children.append(GoalNode(goal=subgoal))

    def mark_completed(self, goal_id: str) -> None:
        """Mark the given goal node as completed."""
        node = self.find_node(goal_id)
        if node is None:
            raise ValueError(f"Goal_id not found: {goal_id}")
        node.completed = True

    def get_open_goals(self) -> list[GoalNode]:
        """Return currently open leaf-like goals."""
        open_nodes: list[GoalNode] = []
        for node in self._dfs_nodes(self.root):
            if node.completed:
                continue
            if any((not child.completed) for child in node.children):
                continue
            open_nodes.append(node)
        return open_nodes

    def print_tree(self) -> None:
        """Print the goal hierarchy."""
        for line in self._format_tree(self.root):
            print(line)

    def _dfs_find(self, node: GoalNode, goal_id: str) -> Optional[GoalNode]:
        if node.goal.goal_id == goal_id:
            return node
        for child in node.children:
            found = self._dfs_find(child, goal_id)
            if found is not None:
                return found
        return None

    def _dfs_nodes(self, node: GoalNode) -> list[GoalNode]:
        out = [node]
        for child in node.children:
            out.extend(self._dfs_nodes(child))
        return out

    def _format_tree(self, node: GoalNode) -> list[str]:
        label = f"Goal: {node.goal.description}"
        if node.completed:
            label += " [DONE]"

        if not node.children:
            return [label]

        lines = [label]
        count = len(node.children)
        for index, child in enumerate(node.children):
            is_last = index == count - 1
            branch = "└── " if is_last else "├── "
            child_lines = self._format_tree(child)
            lines.append(branch + child_lines[0].replace("Goal: ", ""))
            pad = "    " if is_last else "│   "
            for rest in child_lines[1:]:
                lines.append(pad + rest.replace("Goal: ", ""))
        return lines
