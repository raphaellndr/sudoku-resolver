"""AC-3 tests module."""

import copy

from sudoku_resolver.algorithms.ac3 import enforce_arc_consistency
from sudoku_resolver.sudoku import Sudoku
from tests import SUDOKU_PATH

# Row 0 leaves {7, 8, 9} for its last two cells while columns 7 and 8 both forbid 9,
# forcing two 8s in the same row: consistent givens, but no solution.
CONTRADICTORY_SUDOKU = "1234567.." + "." * 18 + ".......9." + "." * 18 + "........9" + "." * 18


def test_enforce_arc_consistency_prunes_domains() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    grid = sudoku.grid
    before = copy.deepcopy(grid.domains.domains)

    assert enforce_arc_consistency(grid)

    after = grid.domains.domains
    assert after != before
    for i in range(9):
        for j in range(9):
            if before[i][j] is not None:
                assert after[i][j]
                assert after[i][j] <= before[i][j]  # type: ignore[operator]


def test_enforce_arc_consistency_contradiction() -> None:
    sudoku = Sudoku.from_string(CONTRADICTORY_SUDOKU)

    assert not enforce_arc_consistency(sudoku.grid)
