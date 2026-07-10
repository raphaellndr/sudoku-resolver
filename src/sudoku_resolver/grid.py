"""Module defining a sudoku grid."""

import numpy as np
from numpy import typing as npt

from .domains import Domains
from .exceptions import ValueAssignmentError

type Index = tuple[int, int]


def _compute_neighbours(value_index: Index) -> tuple[Index, ...]:
    """Computes the indexes sharing a row, column or subgrid with the given index.

    :param value_index: index to compute the neighbours of.
    :returns: deduplicated neighbours indexes.
    """
    i, j = value_index
    row = [(i, j_) for j_ in range(9)]
    column = [(i_, j) for i_ in range(9)]
    subgrid = [
        (i_, j_)
        for i_ in range(i // 3 * 3, i // 3 * 3 + 3)
        for j_ in range(j // 3 * 3, j // 3 * 3 + 3)
    ]
    return tuple(dict.fromkeys(index for index in row + column + subgrid if index != value_index))


NEIGHBOURS: dict[Index, tuple[Index, ...]] = {
    (i, j): _compute_neighbours((i, j)) for i in range(9) for j in range(9)
}


class Grid:
    """Sudoku grid containing all values."""

    def __init__(self, values: npt.NDArray[np.uint8]) -> None:
        self._values = values
        self._initial_assigned_values_indexes: set[Index] = {
            (int(i), int(j)) for i, j in np.argwhere(values != 0)
        }
        self._unassigned: set[Index] = set(NEIGHBOURS) - self._initial_assigned_values_indexes

        self.domains = Domains()
        self.preprocess_domains(self.domains)

    @property
    def unassigned(self) -> set[Index]:
        """Returns the unassigned values indexes as a set. Must not be mutated by callers."""
        return self._unassigned

    @property
    def unassigned_values_indexes(self) -> list[Index]:
        """Returns unassigned values indexes."""
        return sorted(self._unassigned)

    @property
    def assigned_values_indexes(self) -> list[Index]:
        """Returns assigned values indexes."""
        return sorted(set(NEIGHBOURS) - self._unassigned)

    def get_value(self, value_index: Index, /) -> int:
        """Gets the value at given index.

        :param value_index: index of the value to get.
        :returns: value at given index.
        """
        return int(self._values[value_index])

    def set_value(self, value: int, value_index: Index) -> None:
        """Sets the value at given index.

        :param value: value to set.
        :param value_index: index of the value to set.
        :raises ValueAssignmentError: when the index holds an initial value.
        """
        if value_index in self._initial_assigned_values_indexes:
            raise ValueAssignmentError(value_index)
        self._values[value_index] = value
        if value == 0:
            self._unassigned.add(value_index)
        else:
            self._unassigned.discard(value_index)

    def reinitialize_value(self, value_index: Index, /) -> None:
        """Reinitializes a value (sets it to 0).

        :param value_index: index of the value to reinitialize.
        """
        self.set_value(0, value_index)

    def preprocess_domains(self, domains: Domains) -> None:
        """Removes inconsistent values from domains.

        :param domains: domains to clean.
        """
        for index in self.assigned_values_indexes:
            domains.set_domain(None, index)
        for index in self.unassigned_values_indexes:
            neighbour_values = set()
            for neighbour_index in NEIGHBOURS[index]:
                if domains.get_domain(neighbour_index) is None:
                    neighbour_values.add(self.get_value(neighbour_index))
            domains.domains[index[0]][index[1]] -= neighbour_values  # type: ignore[operator]

    def get_horizontal_neighbours_indexes(self, value_index: Index, /) -> list[Index]:
        """Gets horizontal neighbours indexes.

        :param value_index: index of the value to get neighbours indexes from.
        :returns: list containing neighbours' indexes in the row.
        """
        i = value_index[0]
        return [(i, j) for j in range(9) if (i, j) != value_index]

    def get_vertical_neighbours_indexes(self, value_index: Index, /) -> list[Index]:
        """Gets vertical neighbours indexes.

        :param value_index: index of the value to get neighbours indexes from.
        :returns: list containing neighbours' indexes in the column.
        """
        j = value_index[1]
        return [(i, j) for i in range(9) if (i, j) != value_index]

    def get_subgrid_neighbours_indexes(self, value_index: Index, /) -> list[Index]:
        """Gets subgrid neighbours indexes.

        :param value_index: index of the value to get the subgrid neighbours indexes from.
        :returns: list containing neighbours' indexes in the subgrid.
        """
        i, j = value_index
        return [
            (i_, j_)
            for i_ in range(i // 3 * 3, i // 3 * 3 + 3)
            for j_ in range(j // 3 * 3, j // 3 * 3 + 3)
            if (i_, j_) != (i, j)
        ]

    def get_neighbours_indexes(self, value_index: Index, /) -> list[Index]:
        """Gets all neighbours indexes.

        :param value_index: index of the value to get the neighbours indexes from.
        :returns: list containing every indexes.
        """
        return list(NEIGHBOURS[value_index])

    def get_neighbours_values(self, value_index: Index, /) -> list[int]:
        """Gets all neighbours values.

        :param value_index: index of the value to get the neighbours values from.
        :returns: list containing every values.
        """
        return [self.get_value(index) for index in NEIGHBOURS[value_index]]

    def check_constraints(self, *, value: int, value_index: Index) -> bool:
        """Checks if every constraint is respected for a given value.

        :param value: value to check in the grid.
        :param value_index: index of the value to check.
        :returns: `True` if every contraint is respected, `False` otherwise.
        """
        return value not in self.get_neighbours_values(value_index)
