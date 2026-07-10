"""Module defining a Sudoku and its solving methods."""

from pathlib import Path

import numpy as np

from .algorithms import SolverConfig, backtracking
from .exceptions import ConsistencyError, UnsolvableSudokuError
from .grid import Grid


class Sudoku:
    """Represents a Sudoku."""

    def __init__(self, *, values: str | None = None, filepath: str | Path | None = None) -> None:
        """Initializes the Sudoku object.

        :param values: Sudoku grid as a string.
        :param filepath: Path to the file containing the Sudoku grid.
        """
        if values is not None:
            values = values.replace(".", "0")
            self._values = np.array(list(values), dtype=np.uint8).reshape(9, 9)
        elif filepath is not None:
            if isinstance(filepath, str):
                filepath = Path(filepath)
            self._values = self._parse_file(filepath)
        else:
            error_msg = "Either values or filepath must be provided"
            raise ValueError(error_msg)

        self._grid = Grid(self._values)

    @property
    def grid(self) -> Grid:
        """Returns the Sudoku grid."""
        return self._grid

    @classmethod
    def from_file(cls, filepath: str | Path) -> "Sudoku":
        """Alternative constructor to create a Sudoku from a file.

        :param filepath: Path to the file containing the Sudoku.
        :returns: `Sudoku`.
        """
        return cls(filepath=filepath)

    @classmethod
    def from_string(cls, values: str) -> "Sudoku":
        """Alternative constructor to create a Sudoku from a string.

        :param values: Sudoku grid as a string.
        :returns: `Sudoku`.
        """
        return cls(values=values)

    def _parse_file(self, filepath: Path) -> np.ndarray[tuple[int, int], np.dtype[np.uint8]]:
        """Gets values contained in raw file.

        Each dot is converted to a 0.

        :param filepath: path to the file containing the Sudoku grid.
        :returns: `np.ndarray` containing converted values.
        """
        with Path.open(filepath, encoding="utf-8") as stream:
            lines = [line.strip() for line in stream.readlines()]
        array = np.array(
            [[int(c) if c != "." else 0 for c in line] for line in lines],
            dtype=np.uint8,
        )
        if array.shape != (9, 9):
            error_message = "Invalid Sudoku file"
            raise ValueError(error_message)
        return array.reshape(9, 9)

    def solve(self, config: SolverConfig | None = None) -> None:
        """Solves the sudoku in place with a backtracking search.

        :param config: solving techniques to use; defaults to all enabled.
        :raises UnsolvableSudokuError: when the sudoku admits no solution.
        """
        if not backtracking(grid=self._grid, config=config):
            raise UnsolvableSudokuError

    def check_consistency(self) -> bool:
        """Checks if the sudoku is consistent.

        :returns: `True` if the sudoku is consistent, `False` otherwise.
        :raises: `ConsistencyError` if sudoku is inconsistent.
        """
        for index in self.grid.assigned_values_indexes:
            value = self.grid.get_value(index)
            if not self.grid.check_constraints(value=value, value_index=index):
                raise ConsistencyError(value_index=index)
        return True

    def humanize(self) -> str:
        """Renders the grid in a more readable way.

        :returns: formatted sudoku.
        """
        formatted_sudoku = ""
        for i, row in enumerate(self._values):
            if i % 3 == 0 and i != 0:
                formatted_sudoku += "-" * 21 + "\n"
            formatted_sudoku += (
                " ".join(map(str, row[:3]))
                + " | "
                + " ".join(map(str, row[3:6]))
                + " | "
                + " ".join(map(str, row[6:]))
                + "\n"
            )

        return formatted_sudoku

    def to_string(self) -> str:
        """Converts the Sudoku to a string representation.

        :returns: String of 81 characters representing the Sudoku.
        """
        return "".join(str(val) for val in self._values.flatten())

    def save(self, filepath: str | Path) -> None:
        """Saves the Sudoku to a file.

        :param filepath: Path where the Sudoku will be saved.
        """
        path = Path(filepath) if isinstance(filepath, str) else filepath
        path.parent.mkdir(parents=True, exist_ok=True)

        formatted = ""
        for row in self._values:
            formatted += "".join(str(val) if val != 0 else "." for val in row) + "\n"

        with Path.open(path, "w", encoding="utf-8") as f:
            f.write(formatted)

    def __str__(self) -> str:
        return self.humanize()
