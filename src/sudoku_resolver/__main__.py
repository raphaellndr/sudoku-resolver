"""Main module."""

from . import cli


def main() -> None:
    """Main function."""
    # click injects the arguments at parse time
    cli.app()  # pylint: disable=no-value-for-parameter,missing-kwoa


if __name__ == "__main__":
    main()
