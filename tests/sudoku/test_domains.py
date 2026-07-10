"""Domains tests module."""

import re

import pytest

from sudoku_resolver.domains import Domain
from sudoku_resolver.grid import Index
from sudoku_resolver.sudoku import Sudoku
from tests import SUDOKU_PATH


@pytest.mark.parametrize(
    "domain_index,expected_domain",
    [
        ((0, 0), None),
        ((3, 7), {1, 5, 6, 9}),
    ],
)
def test_get_domain(domain_index: Index, expected_domain: Domain | None) -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    domain = sudoku.grid.domains.get_domain(domain_index)

    assert domain == expected_domain


@pytest.mark.parametrize(
    "domain_index,expected_domain",
    [
        ((0, 1), {1}),
        ((3, 7), {1, 2, 3, 9}),
    ],
)
def test_set_domain(domain_index: Index, expected_domain: Domain | None) -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)
    sudoku.grid.domains.set_domain(expected_domain, domain_index)

    assert sudoku.grid.domains.get_domain(domain_index) == expected_domain


def test_set_none_domain() -> None:
    sudoku = Sudoku.from_file(SUDOKU_PATH)

    with pytest.raises(ValueError, match=re.escape("Tried to set a 'None' domain at '(0, 0)'")):
        sudoku.grid.domains.set_domain(set(), (0, 0))
