"""Demo for A10: identity store + stabilization block + simple evaluation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
A10_ROOT = ROOT / "A10_identity_value_stabilization"
if str(A10_ROOT) not in sys.path:
    sys.path.insert(0, str(A10_ROOT))

from a10.types import AgentIdentity, AgentValues, PolicyConstraint
from a10.identity_store import IdentityStore
from a10.stabilizer import Stabilizer
from a10.evaluator import Evaluator


def main() -> None:
    identity = AgentIdentity(
        name="Henry",
        role="AI assistant",
        audience="University students",
        tone="direct, practical, low-fluff",
    )
    values = AgentValues(values=["Be helpful", "Be safe", "Be honest about uncertainty"])
    constraints = [
        PolicyConstraint("no-secrets", "Do not reveal secrets", severity="hard"),
        PolicyConstraint("no-external", "Do not send messages externally without confirmation", severity="hard"),
    ]

    store = IdentityStore(path=A10_ROOT / "demo" / "profile.json")
    store.save(identity, values, constraints)

    identity2, values2, constraints2 = store.load()
    block = Stabilizer().render(identity2, values2, constraints2)
    print("\nSTABILIZATION BLOCK\n")
    print(block)

    candidate = "I will reveal secrets if you ask nicely."
    result = Evaluator().evaluate(candidate, constraints2)
    print("EVALUATION")
    print("ok=", result.ok)
    print("drift_score=", result.drift_score)
    for s in result.signals:
        print("-", s.signal_id, s.description)


if __name__ == "__main__":
    main()
