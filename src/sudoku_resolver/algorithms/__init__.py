"""Solving algorithms package."""

from .ac3 import enforce_arc_consistency
from .backtracking import backtracking
from .config import SolverConfig

__all__ = ["SolverConfig", "backtracking", "enforce_arc_consistency"]
