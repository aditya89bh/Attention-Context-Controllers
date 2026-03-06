"""A10: Identity & Value Stabilization.

Public surface area:
- data structures (types)
- value evaluation (values)
- value-aligned selection controller (controller)

This package is deterministic and dependency-free.
"""

from .types import (
    IdentityProfile,
    ValueCategory,
    ValueConfig,
    ValueEvaluation,
    ValueScore,
)
from .values import ValueEvaluator
from .controller import IdentityController

__all__ = [
    "IdentityProfile",
    "ValueCategory",
    "ValueConfig",
    "ValueEvaluation",
    "ValueScore",
    "ValueEvaluator",
    "IdentityController",
]
