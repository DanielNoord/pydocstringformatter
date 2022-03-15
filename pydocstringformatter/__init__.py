# pylint: disable = import-outside-toplevel

import sys
from typing import List, Union

from pydocstringformatter.utils.exceptions import (
    ParsingError,
    PydocstringFormatterError,
)

__version__ = "0.5.1"


def run_docstring_formatter(argv: Union[List[str], None] = None) -> None:
    """Run the formatter."""
    from pydocstringformatter.run import _Run

    _Run(argv or sys.argv[1:])


__all__ = ("run_docstring_formatter", "PydocstringFormatterError", "ParsingError")
