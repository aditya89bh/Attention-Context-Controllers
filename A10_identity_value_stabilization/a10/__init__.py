"""A10: Identity & Value Stabilization.

Public surface area:
- data structures (types)
- identity store (identity_store)
- stabilizer rules (stabilizer)
- evaluator/drift scoring (evaluator)

This package is deterministic and dependency-free.
"""

from .types import (
    AgentIdentity,
    AgentValues,
    PolicyConstraint,
    DriftSignal,
    EvaluationResult,
)
from .identity_store import IdentityStore
from .stabilizer import Stabilizer
from .evaluator import Evaluator

__all__ = [
    "AgentIdentity",
    "AgentValues",
    "PolicyConstraint",
    "DriftSignal",
    "EvaluationResult",
    "IdentityStore",
    "Stabilizer",
    "Evaluator",
]
