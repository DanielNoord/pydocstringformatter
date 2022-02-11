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
            arguments.append(formatter.deactivate_option)
        elif not formatter.optional:
            arguments.append(formatter.activate_option)

    parser.parse_known_args(arguments, namespace)


def _register_arguments_formatters(
    default_arg_group: argparse._ArgumentGroup,
    optional_arg_group: argparse._ArgumentGroup,
    formatters: List[Formatter],
) -> None:
    """Register a list of formatters, so they can all be deactivated or activated."""
    for formatter in formatters:
        arg_group = default_arg_group
        if formatter.optional:
            arg_group = optional_arg_group

        name = formatter.name
        help_text = f"ctivate the {name} formatter"
        arg_group.add_argument(
            formatter.activate_option,
            action="store_true",
            dest=name,
            help=f"A{help_text} : {formatter.__doc__}",
        )
        arg_group.add_argument(
            formatter.deactivate_option,
            action="store_false",
            dest=name,
            help=f"Dea{help_text}.",
        )
