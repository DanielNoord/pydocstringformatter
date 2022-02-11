import argparse
from typing import List

from pydocstringformatter.configuration import (
    command_line_parsing,
    formatter_options,
    toml_parsing,
)
from pydocstringformatter.configuration.validators import VALIDATORS
from pydocstringformatter.formatting.base import Formatter


class ArgumentsManager:
    """Handler for arugments adding and parsing."""

    def __init__(self, version: str, formatters: List[Formatter]) -> None:
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
        self._register_arguments(version)
        formatter_options._register_arguments_formatters(
            self.default_formatters_group,
            self.optional_formatters_group,
            self.formatters,
        )

    def _register_arguments(self, version: str) -> None:
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

    def parse_options(
        self,
        argv: List[str],
    ) -> None:
        """Load all default option values.

        The order of parsing is:
        1. default values, 2. configuration files, 3. command line arguments.
        """
        # pylint: disable=protected-access
        formatter_options._load_formatters_default_option(
            self.parser, self.namespace, self.formatters
        )

        toml_parsing._parse_toml_file(self.parser, self.namespace)

        command_line_parsing._parse_command_line_arguments(
            self.parser, self.namespace, argv
        )

    def print_help(self) -> None:
        """Print the help or usage message."""
        self.parser.print_help()
