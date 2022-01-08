__all__ = ["FORMATTERS", "Formatter"]

from typing import List

from pydocstringformatter.formatting.base import Formatter
from pydocstringformatter.formatting.formatter import (
    BeginningQuotesFormatter,
    ClosingQuotesFormatter,
    FinalPeriodFormatter,
)

FORMATTERS: List[Formatter] = [
    BeginningQuotesFormatter(),
    ClosingQuotesFormatter(),
    FinalPeriodFormatter(),
]
