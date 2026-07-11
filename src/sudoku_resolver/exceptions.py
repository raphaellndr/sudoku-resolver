"""Module defining custom exceptions."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .grid import Index

__all__ = ["ConsistencyError", "UnsolvableSudokuError", "ValueAssignmentError"]


class ConsistencyError(Exception):
    """Sudoku consistency error.

    Raised when a sudoku doesn't respect all constraints.
    """

    def __init__(self, *, value_index: "Index") -> None:
        self.value_index = value_index

    def __str__(self) -> str:
        """Returns the error message."""
        return (
            f"Sudoku isn't consistent. Value at index '{self.value_index}' "
            "does't respect every constraint"
        )


class UnsolvableSudokuError(Exception):
    """Unsolvable sudoku error.

    Raised when a sudoku admits no solution.
    """

    def __str__(self) -> str:
        """Returns the error message."""
        return "Sudoku has no solution"


class ValueAssignmentError(Exception):
    """Value assignment error.

    Raised when the assignment of a value fails.
    """

    def __init__(self, value_index: "Index") -> None:
        self.value_index = value_index

    def __str__(self) -> str:
        """Returns the error message."""
        return f"Failed to assign a value at given index '{self.value_index}'"
