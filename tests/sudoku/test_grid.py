"""Grid tests module."""

from contextlib import nullcontext as does_not_raise

import pytest

from sudoku_resolver.exceptions import ValueAssignmentError
from sudoku_resolver.grid import Index
from sudoku_resolver.sudoku import Sudoku
from tests import SUDOKU_PATH


@pytest.mark.parametrize(
    "value_index,expected_value",
    [((0, 0), 6), ((2, 1), 0), ((5, 4), 0)],
)
def test_get_value(value_index: Index, expected_value: int) -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    value = sudoku.grid.get_value(value_index)

    assert value == expected_value


@pytest.mark.parametrize(
    "new_value,value_index,expectation",
    [
        (0, (0, 0), pytest.raises(ValueAssignmentError)),
        (8, (2, 1), does_not_raise()),
        (3, (5, 4), does_not_raise()),
    ],
)
def test_set_value(new_value: int, value_index: Index, expectation) -> None:
    with expectation:
        sudoku = Sudoku.from_file(SUDOKU_PATH)
        sudoku.grid.set_value(new_value, value_index)
        value = sudoku.grid.get_value(value_index)

        assert value == new_value


def test_initialize_domains() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)

    assert sudoku.grid.domains.domains == [
        [
            None,
            {7, 8, 9},
            None,
            {8, 9},
            None,
            None,
            None,
            None,
            {9},
        ],
        [
            {8, 9},
            None,
            {4, 8, 9},
            None,
            None,
            {5, 8, 9},
            {4, 6, 9},
            None,
            {5, 6, 9},
        ],
        [
            None,
            {3, 4, 7, 8, 9},
            {3, 4, 7, 8, 9},
            {5, 8, 9},
            {5, 7, 8, 9},
            None,
            {4, 9},
            {2, 5, 8, 9},
            {2, 5, 9},
        ],
        [
            None,
            {1, 4, 5, 6, 8, 9},
            {2, 4, 6, 8, 9},
            None,
            {1, 5, 6, 8, 9},
            {1, 4, 5, 8, 9},
            {6, 9},
            {1, 5, 6, 9},
            {1, 5, 6, 9},
        ],
        [
            {2, 5, 7, 9},
            {1, 4, 5, 6, 7, 9},
            {2, 4, 6, 7, 9},
            {2, 4, 5, 6, 9},
            {1, 5, 6, 9},
            {1, 3, 4, 5, 9},
            None,
            {1, 5, 6, 9},
            {1, 3, 5, 6, 7, 9},
        ],
        [
            {5, 7, 8, 9},
            {1, 5, 6, 7, 8, 9},
            {6, 7, 8, 9},
            {5, 6, 8, 9},
            {1, 5, 6, 8, 9},
            {1, 3, 5, 8, 9},
            None,
            None,
            {1, 3, 5, 6, 7, 9},
        ],
        [
            {5, 7, 8, 9},
            {3, 5, 6, 7, 8, 9},
            None,
            {4, 5, 6, 8, 9},
            None,
            {4, 5, 8, 9},
            {3, 6, 7, 9},
            {6, 9},
            {3, 6, 7, 9},
        ],
        [
            {2, 5, 8, 9},
            {3, 5, 6, 8, 9},
            {2, 3, 6, 8, 9},
            {5, 6, 8, 9},
            {1, 5, 6, 8, 9},
            None,
            {3, 6, 9},
            {1, 2, 6, 9},
            None,
        ],
        [
            None,
            {6, 7, 9},
            {2, 6, 7, 9},
            None,
            {1, 6, 9},
            {1, 9},
            None,
            {1, 2, 6, 9},
            None,
        ],
    ]


@pytest.mark.parametrize(
    "value_index,expected_indexes",
    [
        ((0, 1), [(0, j) for j in range(9) if j != 1]),
        ((2, 4), [(2, j) for j in range(9) if j != 4]),
        ((8, 4), [(8, j) for j in range(9) if j != 4]),
    ],
)
def test_get_horizontal_neighbours_indexes(
    value_index: Index, expected_indexes: list[Index]
) -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    horizontal_neighbours_indexes = sudoku.grid.get_horizontal_neighbours_indexes(value_index)

    assert horizontal_neighbours_indexes == expected_indexes


@pytest.mark.parametrize(
    "value_index,expected_indexes",
    [
        ((0, 1), [(i, 1) for i in range(9) if i != 0]),
        ((2, 4), [(i, 4) for i in range(9) if i != 2]),
        ((8, 4), [(i, 4) for i in range(9) if i != 8]),
    ],
)
def test_get_vertical_neighbours_indexes(value_index: Index, expected_indexes: list[Index]) -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    vertical_neighbours_indexes = sudoku.grid.get_vertical_neighbours_indexes(value_index)

    assert vertical_neighbours_indexes == expected_indexes


@pytest.mark.parametrize(
    "value_index,expected_indexes",
    [
        ((0, 1), [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]),
        ((2, 4), [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 5)]),
        ((8, 4), [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 5)]),
    ],
)
def test_get_subgrid_neighbours_indexes(value_index: Index, expected_indexes: list[Index]) -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    subgrid_neighbours_indexes = sudoku.grid.get_subgrid_neighbours_indexes(value_index)

    assert subgrid_neighbours_indexes == expected_indexes


@pytest.mark.parametrize(
    "value_index,expected_neighbours",
    [
        (
            (0, 1),
            [
                (0, 0),
                (0, 2),
                (0, 3),
                (0, 4),
                (0, 5),
                (0, 6),
                (0, 7),
                (0, 8),
                (1, 0),
                (1, 1),
                (1, 2),
                (2, 0),
                (2, 1),
                (2, 2),
                (3, 1),
                (4, 1),
                (5, 1),
                (6, 1),
                (7, 1),
                (8, 1),
            ],
        ),
        (
            (8, 7),
            [
                (0, 7),
                (1, 7),
                (2, 7),
                (3, 7),
                (4, 7),
                (5, 7),
                (6, 6),
                (6, 7),
                (6, 8),
                (7, 6),
                (7, 7),
                (7, 8),
                (8, 0),
                (8, 1),
                (8, 2),
                (8, 3),
                (8, 4),
                (8, 5),
                (8, 6),
                (8, 8),
            ],
        ),
    ],
)
def test_get_neighbours_indexes(value_index: Index, expected_neighbours: list[Index]) -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    neighbours = sudoku.grid.get_neighbours_indexes(value_index)

    assert sorted(neighbours) == expected_neighbours


@pytest.mark.parametrize(
    "value_index,expected_values",
    [
        (
            (0, 1),
            [0, 0, 5, 2, 0, 0, 0, 0, 3, 0, 4, 0, 0, 0, 6, 0, 2, 0, 1, 1],
        ),
        (
            (8, 7),
            [0, 4, 4, 3, 5, 0, 0, 0, 0, 8, 3, 0, 0, 0, 0, 0, 0, 7, 0, 4],
        ),
    ],
)
def test_get_neighbours_values(value_index: Index, expected_values: list[int]) -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    neighbours_values = sudoku.grid.get_neighbours_values(value_index)

    assert sorted(neighbours_values) == sorted(expected_values)


@pytest.mark.parametrize(
    "value,value_index,expected_result",
    [
        (8, (0, 1), True),
        (5, (2, 4), True),
        (3, (8, 4), False),
    ],
)
def test_check_constraints(value: int, value_index: Index, expected_result: bool) -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    constraints = sudoku.grid.check_constraints(value=value, value_index=value_index)

    assert constraints == expected_result
