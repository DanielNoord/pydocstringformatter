from __future__ import annotations

__all__ = ["FORMATTERS", "Formatter"]


from pydocstringformatter.formatting.base import Formatter
from pydocstringformatter.formatting.formatter import (
    BeginningQuotesFormatter,
    CapitalizeFirstLetterFormatter,
    ClosingQuotesFormatter,
    FinalPeriodFormatter,
    LineWrapperFormatter,
    QuotesTypeFormatter,
    SplitSummaryAndDocstringFormatter,
    StripWhitespacesFormatter,
)

# The order of these formatters is important as they are called in order.
# The order is currently:
#   String manipulation such as adding extra new lines
#   Determine if multi-line or single line and position quotes accordingly
#   String manipulation in which being multi-line or single line matters
FORMATTERS: list[Formatter] = [
    SplitSummaryAndDocstringFormatter(),
    StripWhitespacesFormatter(),
    LineWrapperFormatter(),
    BeginningQuotesFormatter(),
    ClosingQuotesFormatter(),
    CapitalizeFirstLetterFormatter(),
    FinalPeriodFormatter(),
    QuotesTypeFormatter(),
]
