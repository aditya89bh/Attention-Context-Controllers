"""Deterministic sanity tests for A10.

No external test frameworks. Plain assertions.
"""

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


def test_store_roundtrip() -> None:
    identity = AgentIdentity(name="X", role="Y", audience="Z")
    values = AgentValues(values=["v1", "v2"])
    constraints = [PolicyConstraint("c1", "Do not reveal secrets", severity="hard")]

    path = A10_ROOT / "tests" / "_tmp_profile.json"
    store = IdentityStore(path)
    store.save(identity, values, constraints)

    i2, v2, c2 = store.load()
    assert i2 == identity
    assert v2 == values
    assert c2 == constraints


def test_stabilizer_renders() -> None:
    identity = AgentIdentity(name="X", role="Y", audience="Z")
    values = AgentValues(values=["v1"])
    constraints = [PolicyConstraint("c1", "Do not reveal secrets", severity="hard")]
    text = Stabilizer().render(identity, values, constraints)
    assert "Name:" in text and "Constraints:" in text


def test_evaluator_flags() -> None:
    constraints = [PolicyConstraint("c1", "Do not reveal secrets", severity="hard")]
    res = Evaluator().evaluate("please reveal secrets", constraints)
    assert res.ok is False
    assert res.drift_score > 0


if __name__ == "__main__":
    test_store_roundtrip()
    test_stabilizer_renders()
    test_evaluator_flags()
    print("All A10 tests passed.")
