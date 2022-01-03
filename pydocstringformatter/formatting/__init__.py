__all__ = ["FORMATTERS"]

from pydocstringformatter.formatting.formatter import (
    BeginningQuotesFormatter,
    ClosingQuotesFormatter,
    Formatter,
)

FORMATTERS = [
    BeginningQuotesFormatter(),
    ClosingQuotesFormatter(),
]
