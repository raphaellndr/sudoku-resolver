"""Command line interface entrypoint."""

from time import time

import click

from sudoku_resolver.algorithms import SolverConfig
from sudoku_resolver.sudoku import Sudoku


@click.command(name="solve")
@click.argument("file_path", type=click.Path(exists=True, dir_okay=False))
@click.option("--no-ac3", is_flag=True, help="Disable the AC-3 preprocessing pass.")
@click.option("--no-mrv", is_flag=True, help="Disable minimum-remaining-values cell selection.")
@click.option("--no-lcv", is_flag=True, help="Disable least-constraining-value ordering.")
def app(file_path: str, *, no_ac3: bool, no_mrv: bool, no_lcv: bool) -> None:
    """Solves a sudoku."""
    config = SolverConfig(ac3=not no_ac3, mrv=not no_mrv, lcv=not no_lcv)
    sudoku = Sudoku.from_file(file_path)
    print(sudoku.humanize())

    start = time()
    sudoku.solve(config)
    sudoku.check_consistency()
    end = time() - start

    print("SOLVED SUDOKU:\n\n" + sudoku.humanize() + "\n")
    print(f"ELAPSED TIME: {end}")
