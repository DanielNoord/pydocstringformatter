from __future__ import annotations

import argparse
from collections.abc import Sequence
from typing import Any, Literal


class BooleanOptionalAction(argparse.Action):
    """Boolean action that combines the '--no' argument.

    This action is directly copied from argparse with minor modifications.
    This action class is only available in 3.9+. Hence the need to backport it.
    """

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        option_strings: Sequence[str],
        dest: str,
        default: bool,
        type: Literal[None] = None,  # pylint: disable=redefined-builtin
        choices: Literal[None] = None,
        required: bool = False,
        help: str | None = None,  # pylint: disable=redefined-builtin
        metavar: Literal[None] = None,
    ) -> None:
        # Non-argparse changes
        assert help, "All BooleanOptionalAction's should have a help message."

        # Rest of implementation directly copied from argparse, expect for the asserts
        _option_strings = []
        for option_string in option_strings:
            _option_strings.append(option_string)

            assert option_string.startswith("--")
            option_string = "--no-" + option_string[2:]
            _option_strings.append(option_string)

        assert help is not None and default is not None
        help += " (default: %(default)s)"

        super().__init__(
            option_strings=_option_strings,
            dest=dest,
            nargs=0,
            default=default,
            type=type,
            choices=choices,
            required=required,
            help=help,
            metavar=metavar,
        )

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        """Store correct value on the namespace object."""
        assert option_string, (
            "BooleanOptionalAction can't be a positional argument. "
            f"Something is wrong with {self.option_strings[0]}"
        )
        assert option_string in self.option_strings
        setattr(namespace, self.dest, not option_string.startswith("--no-"))

    def format_usage(self) -> str:
        """Return usage string."""
        return "  ".join(self.option_strings)
