"""Module implementing the cell selection and value ordering heuristics."""

from collections import Counter

from sudoku_resolver.grid import NEIGHBOURS, Grid, Index

__all__ = ["least_constraining_value", "minimum_remaining_value"]


def minimum_remaining_value(grid: Grid) -> Index | None:
    """Gets the position of the unassigned cell with the smallest domain (MRV).

    Ties are broken by row order.

    :param grid: `Grid` containing the cells to pick from.
    :returns: index of the cell with the smallest domain, `None` when every cell is assigned.
    """
    if not grid.unassigned:
        return None
    return min(
        grid.unassigned,
        key=lambda index: (len(grid.domains.get_domain(index) or ()), index),
    )


def least_constraining_value(grid: Grid, value_index: Index) -> list[int]:
    """Returns the domain values ordered by number of occurrences in neighbours' domains (LCV).

    Values constraining the fewest neighbours come first; ties are broken by value.

    :param grid: `Grid` containing the domains to order.
    :param value_index: index of the value's domain to order.
    :returns: ordered domain values.
    """
    counts: Counter[int] = Counter()
    for neighbour_index in NEIGHBOURS[value_index]:
        domain = grid.domains.get_domain(neighbour_index)
        if domain:
            counts.update(domain)
    return sorted(
        grid.domains.get_domain(value_index) or (), key=lambda value: (counts[value], value)
    )
