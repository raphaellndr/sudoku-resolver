"""Module containing the definition of a domain and its related methods"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sudoku_resolver.grid import Index

type Domain = set[int]


class Domains:
    """Defines the domains of a Sudoku."""

    def __init__(self) -> None:
        self.domains: list[list[Domain | None]] = [
            [set(range(1, 10)) for _ in range(9)] for _ in range(9)
        ]

    def get_domain(self, domain_index: "Index", /) -> Domain | None:
        """Gets domain at given index.

        :param domain_index: index of the domain to get.
        :returns: domain.
        """
        return self.domains[domain_index[0]][domain_index[1]]

    def set_domain(self, domain: Domain | None, domain_index: "Index") -> None:
        """Sets domain at given index.

        :param domain: new domain value.
        :param domain_index: index of the domain to set.
        """
        if self.get_domain(domain_index) is None:
            error_msg = f"Tried to set a 'None' domain at '{domain_index}'"
            raise ValueError(error_msg)
        self.domains[domain_index[0]][domain_index[1]] = domain
