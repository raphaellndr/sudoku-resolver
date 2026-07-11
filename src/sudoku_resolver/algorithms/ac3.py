"""Module implementing the AC-3 arc consistency algorithm."""

from collections import deque

from sudoku_resolver.grid import NEIGHBOURS, Grid, Index

__all__ = ["enforce_arc_consistency"]


def enforce_arc_consistency(grid: Grid) -> bool:
    """Enforces arc-consistency algorithm (AC-3) on the sudoku.

    :param grid: `Grid` containing the sudoku to make arc-consistent.
    :returns: `False` when a domain has been emptied (no solution), `True` otherwise.
    """
    queue: deque[tuple[Index, Index]] = deque()

    for value_index in grid.unassigned_values_indexes:
        for neighbour in NEIGHBOURS[value_index]:
            queue.append((value_index, neighbour))

    while queue:
        value_index, neighbour_index = queue.popleft()
        if _revise(grid, value_index, neighbour_index):
            if not grid.domains.get_domain(value_index):
                return False
            for neighbour in NEIGHBOURS[value_index]:
                queue.append((neighbour, value_index))
    return True


def _revise(grid: Grid, value_index: Index, neighbour_index: Index) -> bool:
    """Removes inconsistent values from the domain of the cell.

    A value is inconsistent when the neighbour's domain is reduced to that single value.

    :param grid: `Grid` containing the domains to revise.
    :param value_index: cell to check for consistency.
    :param neighbour_index: neighbour to check the consistency with.
    :returns: boolean whether a value has been removed or not.
    """
    domain = grid.domains.get_domain(value_index)
    neighbour_domain = grid.domains.get_domain(neighbour_index)
    if domain and neighbour_domain and len(neighbour_domain) == 1:
        (neighbour_value,) = neighbour_domain
        if neighbour_value in domain:
            domain.remove(neighbour_value)
            return True
    return False
