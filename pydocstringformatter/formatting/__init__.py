__all__ = ["FORMATTERS"]

from typing import List

from pydocstringformatter.formatting.formatter import (
    BeginningQuotesFormatter,
    ClosingQuotesFormatter,
    Formatter,
)

FORMATTERS: List[Formatter] = [
    BeginningQuotesFormatter(),
    ClosingQuotesFormatter(),
]
