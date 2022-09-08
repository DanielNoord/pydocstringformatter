from __future__ import annotations

__all__ = ["FORMATTERS", "Formatter"]


from pydocstringformatter._formatting.base import Formatter
from pydocstringformatter._formatting.formatters_default import (
    BeginningQuotesFormatter,
    CapitalizeFirstLetterFormatter,
    ClosingQuotesFormatter,
    FinalPeriodFormatter,
    LineWrapperFormatter,
    QuotesTypeFormatter,
    StripWhitespacesFormatter,
)
from pydocstringformatter._formatting.formatters_numpydoc import (
    NumpydocNameColonTypeFormatter,
    NumpydocSectionHyphenLengthFormatter,
    NumpydocSectionOrderingFormatter,
    NumpydocSectionSpacingFormatter,
)
from pydocstringformatter._formatting.formatters_pep257 import (
    SplitSummaryAndDocstringFormatter,
)

# The order of these formatters is important as they are called in order.
# The order is currently:
#   String manipulation such as adding extra new lines
#   Determine if multi-line or single line and position quotes accordingly
#   String manipulation in which being multi-line or single line matters
FORMATTERS: list[Formatter] = [
    StripWhitespacesFormatter(),
    SplitSummaryAndDocstringFormatter(),
    NumpydocSectionOrderingFormatter(),
    NumpydocNameColonTypeFormatter(),
    NumpydocSectionSpacingFormatter(),
    NumpydocSectionHyphenLengthFormatter(),
    LineWrapperFormatter(),
    BeginningQuotesFormatter(),
    ClosingQuotesFormatter(),
    CapitalizeFirstLetterFormatter(),
    FinalPeriodFormatter(),
    QuotesTypeFormatter(),
]
