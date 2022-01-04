__all__ = ["FORMATTERS"]

from typing import List

from pydocstringformatter.formatting.base import Formatter
from pydocstringformatter.formatting.formatter import (
    BeginningQuotesFormatter,
    ClosingQuotesFormatter,
)

FORMATTERS: List[Formatter] = [
    BeginningQuotesFormatter(),
    ClosingQuotesFormatter(),
]
