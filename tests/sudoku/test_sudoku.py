"""Sudoku tests module."""

from pathlib import Path

import numpy as np
import pytest

from sudoku_resolver.algorithms import SolverConfig
from sudoku_resolver.exceptions import ConsistencyError, UnsolvableSudokuError
from sudoku_resolver.sudoku import Sudoku
from tests import DATA_DIR, SUDOKU_PATH

UNSOLVABLE_SUDOKU = "12345678." + "." * 9 + ".......9." + "." * 54


def test_initialize_values() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)

    assert (
        sudoku.grid._values
        == np.asarray(
            [
                [6, 0, 5, 0, 4, 2, 1, 3, 0],
                [0, 2, 0, 1, 3, 0, 0, 7, 0],
                [1, 0, 0, 0, 0, 6, 0, 0, 0],
                [3, 0, 0, 7, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 8, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 4, 0],
                [0, 0, 1, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 7, 0, 0, 4],
                [4, 0, 0, 3, 0, 0, 5, 0, 8],
            ],
            dtype=np.uint8,
        )
    ).all()


def test_solve_sudoku() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    sudoku.solve()

    assert (
        sudoku.grid._values
        == np.asarray(
            [
                [6, 7, 5, 8, 4, 2, 1, 3, 9],
                [8, 2, 4, 1, 3, 9, 6, 7, 5],
                [1, 9, 3, 5, 7, 6, 4, 8, 2],
                [3, 5, 2, 7, 8, 4, 9, 6, 1],
                [9, 4, 6, 2, 1, 3, 8, 5, 7],
                [7, 1, 8, 9, 6, 5, 2, 4, 3],
                [5, 3, 1, 4, 2, 8, 7, 9, 6],
                [2, 8, 9, 6, 5, 7, 3, 1, 4],
                [4, 6, 7, 3, 9, 1, 5, 2, 8],
            ],
            dtype=np.uint8,
        )
    ).all()


def test_check_consistency() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    sudoku.solve()

    assert sudoku.check_consistency()


def test_check_inconsistency() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    sudoku.solve()
    sudoku.grid._values[0][0] = 1

    with pytest.raises(ConsistencyError):
        sudoku.check_consistency()


def test_humanize() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    sudoku.solve()

    assert (
        sudoku.humanize() == "6 7 5 | 8 4 2 | 1 3 9\n"
        "8 2 4 | 1 3 9 | 6 7 5\n"
        "1 9 3 | 5 7 6 | 4 8 2\n"
        "---------------------\n"
        "3 5 2 | 7 8 4 | 9 6 1\n"
        "9 4 6 | 2 1 3 | 8 5 7\n"
        "7 1 8 | 9 6 5 | 2 4 3\n"
        "---------------------\n"
        "5 3 1 | 4 2 8 | 7 9 6\n"
        "2 8 9 | 6 5 7 | 3 1 4\n"
        "4 6 7 | 3 9 1 | 5 2 8\n"
    )


@pytest.mark.parametrize(
    "puzzle_path",
    sorted(DATA_DIR.rglob("*.txt")),
    ids=lambda path: str(path.relative_to(DATA_DIR)),
)
def test_solve_data_puzzles(puzzle_path: Path) -> None:
    sudoku = Sudoku.from_file(puzzle_path)
    sudoku.solve()

    assert sudoku.check_consistency()
    assert "0" not in sudoku.to_string()


@pytest.mark.parametrize(
    "ac3,mrv,lcv",
    [(ac3, mrv, lcv) for ac3 in (True, False) for mrv in (True, False) for lcv in (True, False)],
)
def test_solve_with_config(*, ac3: bool, mrv: bool, lcv: bool) -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    sudoku.solve(SolverConfig(ac3=ac3, mrv=mrv, lcv=lcv))

    assert sudoku.check_consistency()
    assert "0" not in sudoku.to_string()


@pytest.mark.parametrize(
    "config",
    [
        SolverConfig(),
        SolverConfig(ac3=False),
    ],
)
def test_solve_unsolvable_sudoku(config: SolverConfig) -> None:
    sudoku = Sudoku.from_string(UNSOLVABLE_SUDOKU)

    with pytest.raises(UnsolvableSudokuError):
        sudoku.solve(config)


@pytest.mark.timeout(5)
@pytest.mark.parametrize(
    "values",
    [
        "1" + "0" * 80,  # single clue
        "1" + "0" * 79 + "1",  # two clues top-left + bottom-right (previously hung)
        "0" * 81,  # empty grid
    ],
    ids=["single-clue", "two-clue", "empty"],
)
def test_solve_underconstrained_terminates(values: str) -> None:
    sudoku = Sudoku.from_string(values)
    sudoku.solve()

    assert sudoku.check_consistency()
    assert "0" not in sudoku.to_string()


def test_from_string_with_dots() -> None:
    dotted = ".2345678." + "." * 72
    zeroed = "023456780" + "0" * 72

    assert Sudoku.from_string(dotted).to_string() == zeroed
