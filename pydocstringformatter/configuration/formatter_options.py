import argparse
from typing import List

from pydocstringformatter.formatting.base import Formatter


def _load_formatters_default_option(
    parser: argparse.ArgumentParser,
    namespace: argparse.Namespace,
    formatters: List[Formatter],
) -> None:
    """Parse the state of the list of formatters based on their 'optional' attribute."""
    arguments: List[str] = []
    for formatter in formatters:
        if formatter.optional:
            arguments.append(f"--no-{formatter.name}")
        elif not formatter.optional:
            arguments.append(f"--{formatter.name}")

    parser.parse_known_args(arguments, namespace)


def _register_arguments_formatters(
    parser: argparse.ArgumentParser, formatters: List[Formatter]
) -> None:
    """Register a list of formatters, so they can all be deactivated or activated."""
    for formatter in formatters:
        name = formatter.name
        help_text = f"ctivate the {name} formatter"
        parser.add_argument(
            f"--{name}",
            action="store_true",
            dest=name,
            help=f"A{help_text} : {formatter.__doc__}",
        )
        parser.add_argument(
            f"--no-{name}", action="store_false", dest=name, help=f"Dea{help_text}"
        )
