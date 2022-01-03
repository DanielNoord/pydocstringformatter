__all__ = ["FORMATTERS"]

from pydocstringformatter.formatting.formatter import (
    BeginningQuotesFormatter,
    ClosingQuotesFormatter,
)

FORMATTERS = [
    BeginningQuotesFormatter(),
    ClosingQuotesFormatter(),
]
