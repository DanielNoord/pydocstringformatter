__all__ = ["FORMATTERS"]

from typing import List

from pydocstringformatter.formatting.base import Formatter
from pydocstringformatter.formatting.formatter import (
    BeginningQuotesFormatter,
    ClosingQuotesFormatter,
    FinalPeriodFormatter,
    SplitSummaryAndDocstringFormatter,
)

# The order of these formatters is important as they are called in order.
# The order is currently:
#   String manipulation such as adding extra new lines
#   Determine if multi-line or single line and position quotes accordingly
#   String manipulation in which being multi-line or single line matters
FORMATTERS: List[Formatter] = [
    SplitSummaryAndDocstringFormatter(),
    BeginningQuotesFormatter(),
    ClosingQuotesFormatter(),
    FinalPeriodFormatter(),
]
