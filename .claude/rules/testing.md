---
paths:
  - "tests/**/*.py"
---

# Testing conventions (pytest)

- Tests live under `tests/sudoku/`, one `test_<module>.py` per source module.
- Prefer **`@pytest.mark.parametrize`** — that's the established style. Cover the success and the raising paths together using `pytest.raises(...)` vs `contextlib.nullcontext()` (imported as `does_not_raise`) in the same parametrize table.
- The shared sample grid is `tests/data/sudoku.txt`, exposed as `SUDOKU_PATH` in `tests/__init__.py` — use it instead of adding new fixture files.
- Run `scripts/test` or `poetry run pytest`.
