"""CLI tests module."""

import pytest
from click.testing import CliRunner

from sudoku_resolver import cli
from sudoku_resolver.algorithms import SolverConfig
from sudoku_resolver.sudoku import Sudoku
from tests import SUDOKU_PATH


@pytest.mark.parametrize(
    "flags,expected_config",
    [
        ([], SolverConfig()),
        (["--no-ac3"], SolverConfig(ac3=False)),
        (["--no-mrv"], SolverConfig(mrv=False)),
        (["--no-lcv"], SolverConfig(lcv=False)),
        (["--no-ac3", "--no-mrv", "--no-lcv"], SolverConfig(ac3=False, mrv=False, lcv=False)),
    ],
)
def test_cli_solve_flags(
    flags: list[str], expected_config: SolverConfig, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured = {}
    original_solve = Sudoku.solve

    def spy(self: Sudoku, config: SolverConfig | None = None) -> None:
        captured["config"] = config
        original_solve(self, config)

    monkeypatch.setattr(Sudoku, "solve", spy)
    result = CliRunner().invoke(cli.app, [str(SUDOKU_PATH), *flags])

    assert result.exit_code == 0
    assert captured["config"] == expected_config
    assert "SOLVED SUDOKU" in result.output


def test_cli_missing_file() -> None:
    result = CliRunner().invoke(cli.app, ["nonexistent.txt"])

    assert result.exit_code != 0
