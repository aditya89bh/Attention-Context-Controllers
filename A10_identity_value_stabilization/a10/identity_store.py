"""A10 identity store.

A small deterministic file-backed store for identity/values/policies.

Design goals:
- transparent (human-readable JSON)
- deterministic load/save
- no external dependencies
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .types import AgentIdentity, AgentValues, PolicyConstraint


class IdentityStore:
    """Read/write identity, values, and constraints to a JSON file."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save(
        self,
        identity: AgentIdentity,
        values: AgentValues,
        constraints: list[PolicyConstraint],
    ) -> None:
        """Persist the profile to disk."""
        payload = {
            "identity": asdict(identity),
            "values": asdict(values),
            "constraints": [asdict(c) for c in constraints],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    def load(self) -> tuple[AgentIdentity, AgentValues, list[PolicyConstraint]]:
        """Load the profile from disk."""
        payload = json.loads(self.path.read_text())
        identity = AgentIdentity(**payload["identity"])
        values = AgentValues(**payload["values"])
        constraints = [PolicyConstraint(**c) for c in payload["constraints"]]
        return identity, values, constraints
