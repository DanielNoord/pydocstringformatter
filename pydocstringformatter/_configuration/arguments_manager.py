from __future__ import annotations

import argparse

from pydocstringformatter._configuration import (
    command_line_parsing,
    formatter_options,
    toml_parsing,
)
from pydocstringformatter._configuration.validators import VALIDATORS
from pydocstringformatter._formatting.base import Formatter


class ArgumentsManager:
    """Handler for arugments adding and parsing."""

    def __init__(self, version: str, formatters: list[Formatter]) -> None:
        # Initialize instance attributes for argument parsing
        self.parser = argparse.ArgumentParser(prog="pydocstringformatter")
        self.namespace = argparse.Namespace()

        self.formatters = formatters
        """List of loaded formatters."""

        # First register all argument groups, then add arguments
        self.configuration_group = self.parser.add_argument_group("configuration")
        self.default_formatters_group = self.parser.add_argument_group(
            "default formatters", "these formatters are turned on by default"
        )
        self.optional_formatters_group = self.parser.add_argument_group(
            "optional formatters", "these formatters are turned off by default"
        )

        # Register all arguments
        self.register_arguments(version)
        formatter_options.register_arguments_formatters(
            self.default_formatters_group,
            self.optional_formatters_group,
            self.formatters,
        )

    def register_arguments(self, version: str) -> None:
        """Register all standard arguments on the parser."""
        self.parser.add_argument(
            "files", nargs="*", type=str, help="The directory or files to format."
        )

        self.parser.add_argument(
            "-w",
            "--write",
            action="store_true",
            help="Write the changes to file instead of printing the diffs to stdout.",
        )

        self.parser.add_argument(
            "--quiet",
            action="store_true",
            help="Do not print any logging or status messages to stdout.",
        )

        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=version,
            help="Show version number and exit.",
        )

        self.configuration_group.add_argument(
            "--exclude",
            action="store",
            default=[""],
            type=VALIDATORS["csv"],
            help=(
                "A comma separated list of glob patterns of "
                "file path names not to be formatted."
            ),
        )

        self.configuration_group.add_argument(
            "--exit-code",
            action="store_true",
            default=False,
            help=(
                "Turn on if the program should exit with bitwise exit codes. "
                "0 = No changes, 32 = Changed files or printed diff."
            ),
        )

        self.configuration_group.add_argument(
            "--max-summary-lines",
            action="store",
            default=1,
            type=int,
            help=(
                "The maximum numbers of lines a summary can span. "
                "The default value is 1."
            ),
            metavar="int",
        )

        self.configuration_group.add_argument(
            "--summary-quotes-same-line",
            action="store_true",
            help=(
                "Force the start of a multi-line docstring to be on the "
                "same line as the opening quotes. Similar to how this is enforced "
                "for single line docstrings."
            ),
        )

        self.configuration_group.add_argument(
            "--max-line-length",
            action="store",
            default=88,
            type=int,
            help="Maximum line length of docstrings.",
            metavar="int",
        )

        self.configuration_group.add_argument(
            "--style",
            action="extend",
            type=str,
            nargs="+",
            choices=["pep257", "numpydoc"],
            help="Docstring styles that are used in the project. Can be more than one.",
        )

    def parse_options(
        self,
        argv: list[str],
    ) -> None:
        """Load all default option values.

        The order of parsing is:
        1. configuration files, 2. command line arguments, 3. set default values.
        """
        # pylint: disable=protected-access
        toml_parsing.parse_toml_file(self.parser, self.namespace)

        command_line_parsing.parse_command_line_arguments(
            self.parser, self.namespace, argv
        )

        # 'style' uses the 'extend' action. If we use a normal default value,
        # and the default gets supplied as well style == ["pep257", "pep257"].
        if self.namespace.style is None:
            self.namespace.style = ["pep257"]

    def print_help(self) -> None:
        """Print the help or usage message."""
        self.parser.print_help()
