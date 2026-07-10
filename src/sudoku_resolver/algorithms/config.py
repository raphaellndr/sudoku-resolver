"""Module defining the solver configuration."""

from dataclasses import dataclass

__all__ = ["SolverConfig"]


@dataclass(frozen=True)
class SolverConfig:
    """Toggles for the optional solving techniques.

    Forward checking is always on: it is the backbone of the search, not a heuristic.

    :param ac3: runs the AC-3 preprocessing pass before searching.
    :param mrv: picks the cell with the smallest domain first; otherwise the first unassigned
        cell in row order.
    :param lcv: tries the least constraining values first; otherwise ascending order.
    """

    ac3: bool = True
    mrv: bool = True
    lcv: bool = True
