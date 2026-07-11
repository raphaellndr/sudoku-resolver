"""Module implementing the backtracking search with forward checking."""

from sudoku_resolver.grid import NEIGHBOURS, Grid, Index

from .ac3 import enforce_arc_consistency
from .config import SolverConfig
from .heuristics import least_constraining_value, minimum_remaining_value

__all__ = ["backtracking"]


def backtracking(*, grid: Grid, config: SolverConfig | None = None) -> bool:
    """Backtracking search with forward checking for solving Sudoku puzzles.

    :param grid: `Grid` containing the sudoku to solve.
    :param config: solving techniques to use; defaults to all enabled.
    :returns: `True` if a solution has been found, `False` otherwise.
    """
    config = config or SolverConfig()
    if config.ac3 and not enforce_arc_consistency(grid):
        return False
    return _search(grid, config)


def _search(grid: Grid, config: SolverConfig) -> bool:
    """Recursively assigns values to unassigned cells, backtracking on dead ends.

    :param grid: `Grid` containing the sudoku to solve.
    :param config: solving techniques to use.
    :returns: `True` if a solution has been found, `False` otherwise.
    """
    index = _select_cell(grid, config)
    if index is None:
        return True
    for value in _ordered_values(grid, index, config):
        pruned = _assign(grid=grid, value=value, value_index=index)
        if pruned is None:
            continue
        if _search(grid, config):
            return True
        _unassign(grid=grid, value=value, value_index=index, pruned=pruned)
    return False


def _select_cell(grid: Grid, config: SolverConfig) -> Index | None:
    """Picks the next cell to assign.

    :param grid: `Grid` containing the sudoku to solve.
    :param config: solving techniques to use.
    :returns: index of the next cell, `None` when every cell is assigned.
    """
    if config.mrv:
        return minimum_remaining_value(grid)
    unassigned = grid.unassigned_values_indexes
    return unassigned[0] if unassigned else None


def _ordered_values(grid: Grid, value_index: Index, config: SolverConfig) -> list[int]:
    """Orders the candidate values of a cell's domain.

    :param grid: `Grid` containing the sudoku to solve.
    :param value_index: index of the cell to order the values of.
    :param config: solving techniques to use.
    :returns: ordered candidate values.
    """
    if config.lcv:
        return least_constraining_value(grid, value_index)
    return sorted(grid.domains.get_domain(value_index) or ())


def _assign(*, grid: Grid, value: int, value_index: Index) -> list[Index] | None:
    """Assigns a value and prunes it from the unassigned neighbours' domains (forward checking).

    :param grid: `Grid` containing the sudoku to solve.
    :param value: value to assign.
    :param value_index: index of the cell to assign the value to.
    :returns: indexes of the pruned domains, `None` when a domain would empty (assignment is
        then fully reverted).
    """
    grid.set_value(value, value_index)
    pruned: list[Index] = []
    for neighbour_index in NEIGHBOURS[value_index]:
        if grid.get_value(neighbour_index) != 0:
            continue
        domain = grid.domains.get_domain(neighbour_index)
        if domain is None or value not in domain:
            continue
        domain.remove(value)
        pruned.append(neighbour_index)
        if not domain:
            _unassign(grid=grid, value=value, value_index=value_index, pruned=pruned)
            return None
    return pruned


def _unassign(*, grid: Grid, value: int, value_index: Index, pruned: list[Index]) -> None:
    """Reverts an assignment and restores the domains it pruned.

    :param grid: `Grid` containing the sudoku to solve.
    :param value: value to revert.
    :param value_index: index of the cell to revert.
    :param pruned: indexes of the domains the assignment pruned.
    """
    for neighbour_index in pruned:
        domain = grid.domains.get_domain(neighbour_index)
        if domain is not None:
            domain.add(value)
    grid.reinitialize_value(value_index)
