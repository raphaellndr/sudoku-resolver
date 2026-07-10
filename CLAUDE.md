# CLAUDE.md

Project context for **sudoku-resolver** (Python 3.12 / Poetry). A CLI that solves 9×9 sudokus by treating them as constraint-satisfaction problems (backtracking + domain pruning). See @README.md for setup.

## Behavioral guidelines

Guidelines to reduce common LLM coding mistakes.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```text
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## Commands

Package manager is **Poetry** (in-project `.venv`). Helper scripts live in `scripts/`.

- `poetry install` — install deps
- `poetry run sudoku-resolver <file>` — solve a sudoku file (samples in `data/`; entrypoint `__main__.py` → `cli.py`, a single click command). `--no-ac3 / --no-mrv / --no-lcv` disable individual solving techniques (for benchmarking/comparison).
- `scripts/codeformatting` — reformat; `scripts/codeformatting check` is check-only
- `scripts/codeanalysis` — mypy + pylint
- `scripts/test` — pytest with coverage (`rm .coverage*` first); or `poetry run pytest` for a plain run
- `scripts/build` — `poetry build`

Git hooks (**pre-commit**): on commit, ruff format + `ruff check --fix` + mypy + pylint + pytest; on push, `pytest --cov`.

## Architecture

Data structures and algorithms are deliberately separated: `grid.py`/`domains.py` hold state, the `algorithms/` package operates on it, and nothing imports back up.

- `sudoku.py` — `Sudoku` façade: parses a grid from an 81-char string or a file (`.` = empty cell), owns a `Grid`, exposes `solve(config)` / `check_consistency()` / `humanize()`.
- `grid.py` — `Grid` wraps the 9×9 numpy `uint8` array: value get/set, unassigned-cell tracking, constraint checks; owns the `Domains` (candidate sets per cell, `None` for initially-given cells). `NEIGHBOURS` is a precomputed module-level map of each cell's 20 peers. `Index` is a `(row, col)` tuple alias.
- `algorithms/` — the solving techniques, as functions taking a `Grid`:
  - `config.py` — `SolverConfig` toggles the optional techniques (`ac3`, `mrv`, `lcv` — all default on; toggles exist for benchmarking and the future API/frontend).
  - `backtracking.py` — recursive backtracking with forward checking (always on, with trail-based undo).
  - `ac3.py` — AC-3 arc consistency preprocessing.
  - `heuristics.py` — MRV cell selection, LCV value ordering.
- `exceptions.py` — `ConsistencyError`, `UnsolvableSudokuError`, `ValueAssignmentError`.
- `cli.py` — click command (single command, invoked without a subcommand name).
- Public API is re-exported at the package root: `from sudoku_resolver import Sudoku, SolverConfig`.

## Conventions

- Docstring format lives in `.claude/rules/docstrings.md`.
- Sudoku file format: 9 lines of 9 characters, digits with `.` for empty cells (see `data/`).

## Key gotchas

- The coverage gate (`fail_under`) is only 10%.
- `ruff check` currently reports pre-existing violations in `src` and `tests` (T201 prints in the CLI, SLF001/PLR2004/FBT001 in tests, EM101/TRY003 in `sudoku.py`) — untriaged lint debt, not regressions.
