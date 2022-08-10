from __future__ import annotations

import argparse

from pydocstringformatter._configuration.boolean_option_action import (
    BooleanOptionalAction,
)
from pydocstringformatter._formatting.base import Formatter


def register_arguments_formatters(
    default_arg_group: argparse._ArgumentGroup,
    optional_arg_group: argparse._ArgumentGroup,
    formatters: list[Formatter],
) -> None:
    """Register a list of formatters, so they can all be deactivated or activated."""
    for formatter in formatters:
        arg_group = default_arg_group
        if formatter.optional:
            arg_group = optional_arg_group

        name = formatter.name
        arg_group.add_argument(
            formatter.activate_option,
            action=BooleanOptionalAction,
            dest=name,
            help=f"Activate or deactivate {name}: {formatter.__doc__}"
            f" Styles: {','.join(formatter.style)}.",
            default=not formatter.optional,
        )
