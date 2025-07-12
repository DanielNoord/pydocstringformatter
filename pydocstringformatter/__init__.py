# pylint: disable = import-outside-toplevel
from __future__ import annotations

import sys

from pydocstringformatter._utils.exceptions import (
    ParsingError,
    PydocstringFormatterError,
)

__version__ = "0.7.5"


def run_docstring_formatter(argv: list[str] | None = None) -> None:
    """Run the formatter."""
    from pydocstringformatter.run import _Run

    _Run(argv or sys.argv[1:])


__all__ = ("run_docstring_formatter", "PydocstringFormatterError", "ParsingError")
