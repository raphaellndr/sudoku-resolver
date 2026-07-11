"""sudoku package root."""

from .algorithms import SolverConfig
from .sudoku import Sudoku

__all__ = ["PROGRAM_NAME", "SolverConfig", "Sudoku", "__version__"]

__version__ = "0.1.0"
PROGRAM_NAME = "sudoku-resolver"
