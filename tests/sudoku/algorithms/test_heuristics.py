"""Heuristics tests module."""

import pytest

from sudoku_resolver.algorithms.heuristics import (
    least_constraining_value,
    minimum_remaining_value,
)
from sudoku_resolver.grid import Index
from sudoku_resolver.sudoku import Sudoku
from tests import SUDOKU_PATH


def test_minimum_remaining_value() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    mrv = minimum_remaining_value(sudoku.grid)

    assert mrv == (0, 8)


def test_minimum_remaining_value_solved_grid() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    sudoku.solve()

    assert minimum_remaining_value(sudoku.grid) is None


@pytest.mark.parametrize(
    "value_index,expected_lcv",
    [
        ((0, 1), [7, 8, 9]),
        ((2, 4), [7, 5, 8, 9]),
        ((8, 4), [1, 6, 9]),
    ],
)
def test_least_constraining_value(value_index: Index, expected_lcv: list[int]) -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    lcv = least_constraining_value(sudoku.grid, value_index)

    assert lcv == expected_lcv
