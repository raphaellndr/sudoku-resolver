# sudoku-resolver

A command line solver for 9x9 sudokus. The grid is treated as a constraint satisfaction
problem: each empty cell keeps the set of values it can still take, and a backtracking
search assigns cells one at a time while pruning the sets of their neighbours.

## Requirements

- Python 3.12
- [Poetry](https://python-poetry.org/docs/#installation)

## Installation

```shell
poetry install
```

The virtual environment is created inside the project (`.venv`).

## Usage

```shell
poetry run sudoku-resolver data/expert/sudoku_1.txt
```

The command prints the puzzle, the solution and how long the search took:

```text
8 0 0 | 0 0 0 | 0 0 6
7 0 0 | 0 0 0 | 5 0 1
9 5 6 | 0 0 0 | 0 2 0
---------------------
0 8 0 | 0 0 0 | 0 0 0
0 0 7 | 9 0 0 | 0 4 0
4 0 0 | 0 0 5 | 1 9 2
---------------------
0 0 0 | 8 1 0 | 0 0 7
1 0 0 | 0 9 0 | 2 0 0
0 0 0 | 6 0 0 | 0 0 0

SOLVED SUDOKU:

8 2 1 | 4 5 7 | 9 3 6
7 3 4 | 2 6 9 | 5 8 1
9 5 6 | 1 3 8 | 7 2 4
---------------------
2 8 9 | 3 4 1 | 6 7 5
5 1 7 | 9 2 6 | 3 4 8
4 6 3 | 7 8 5 | 1 9 2
---------------------
6 9 2 | 8 1 3 | 4 5 7
1 7 8 | 5 9 4 | 2 6 3
3 4 5 | 6 7 2 | 8 1 9

ELAPSED TIME: 0.005500793457031
```

### Input format

A puzzle file holds 9 lines of 9 characters. Empty cells are written `.` or `0`:

```text
6.5.4213.
.2.13..7.
1....6...
3..7.....
......8..
......24.
..1.2....
.....7..4
4..3..5.8
```

Sample puzzles are in [data/](data/), sorted by difficulty (`simple/`, `hard/`, `expert/`).

### Options

Three solving techniques are enabled by default and can be turned off one by one. They are
mostly useful to compare timings on a hard puzzle:

| Flag | Effect |
| --- | --- |
| `--no-ac3` | Skips the AC-3 pass that shrinks the candidate sets before the search starts. |
| `--no-mrv` | Picks the first unassigned cell in row order instead of the one with the fewest candidates. |
| `--no-lcv` | Tries candidate values in ascending order instead of least constraining first. |

```shell
poetry run sudoku-resolver data/expert/sudoku_1.txt --no-mrv --no-lcv
```

## Python API

```python
from sudoku_resolver import SolverConfig, Sudoku

sudoku = Sudoku.from_file("data/simple/sudoku_1.txt")
# or: Sudoku.from_string("6.5.4213..2.13..7.1....6...3..7...........8........24...1.2.........7..44..3..5.8")

sudoku.solve()                      # solves in place
sudoku.solve(SolverConfig(lcv=False))  # same, without the LCV ordering
sudoku.check_consistency()          # raises ConsistencyError if a constraint is broken

print(sudoku.humanize())            # grid with separators, as printed by the CLI
sudoku.to_string()                  # the 81 values on a single line
sudoku.save("solved.txt")           # writes the file format above
```

`solve()` raises `UnsolvableSudokuError` when the puzzle admits no solution. Every exception
lives in `sudoku_resolver.exceptions`.

## How the solver works

Values and algorithms are kept apart: `grid.py` and `domains.py` hold the state, the
`algorithms/` package works on it.

1. **Domain preprocessing.** Every empty cell starts with the candidates 1 to 9, minus the
   values already present in its row, column and 3x3 box. Given cells have no domain.
2. **AC-3** (optional). Whenever a cell has a single candidate left, that value is removed
   from the domains of its 20 peers, and the peers are queued for another check. An empty
   domain at this point means the puzzle has no solution.
3. **Backtracking with forward checking** (always on). A cell is picked, a value assigned,
   and the value removed from the domains of its unassigned peers. If one of these domains
   becomes empty, the assignment is undone right away. The search records what it pruned so
   backtracking restores the exact previous state.
4. **MRV** (optional) picks the cell with the fewest candidates, which fails early instead
   of deep in the recursion.
5. **LCV** (optional) tries first the values that appear the least in the peers' domains,
   so the branches explored first are the ones leaving the most room.

## Development

```shell
poetry run pytest              # tests
poetry run pytest --cov        # tests with coverage
./scripts/code-style           # ruff format + ruff check --fix
./scripts/code-style check     # same, read only
poetry run mypy                # type checking, on src/sudoku_resolver
./scripts/build                # poetry build
```

Git hooks are managed by pre-commit. Formatting, linting and type checking run on commit,
the test suite runs on push:

```shell
poetry run pre-commit install --hook-type pre-commit --hook-type pre-push
```

Tests live in `tests/sudoku/`, one file per module.
