"""A10 stabilizer.

Converts identity/values/constraints into a deterministic "stabilization block"
that can be injected into prompts or used as a control summary.
"""

from __future__ import annotations

from .types import AgentIdentity, AgentValues, PolicyConstraint


class Stabilizer:
    """Deterministically render a stabilization block."""

    def render(
        self,
        identity: AgentIdentity,
        values: AgentValues,
        constraints: list[PolicyConstraint],
    ) -> str:
        """Return a stable text block expressing identity + values + constraints."""
        lines: list[str] = []
        lines.append(f"Name: {identity.name}")
        lines.append(f"Role: {identity.role}")
        lines.append(f"Audience: {identity.audience}")
        lines.append(f"Tone: {identity.tone}")
        lines.append("")

        if values.values:
            lines.append("Values (priority order):")
            for i, v in enumerate(values.values, 1):
                lines.append(f"  {i}. {v}")
            lines.append("")

        if constraints:
            lines.append("Constraints:")
            # Stable ordering: hard first, then soft; then by id
            ordered = sorted(
                constraints,
                key=lambda c: (0 if c.severity == "hard" else 1, c.constraint_id),
            )
            for c in ordered:
                lines.append(f"  - [{c.severity}] {c.text}")

        return "\n".join(lines).strip() + "\n"
