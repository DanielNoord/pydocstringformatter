import abc
import re
import tokenize

# pylint: disable=too-few-public-methods
from typing import List


class Formatter:
    """Base class for docstring formatter"""

    @abc.abstractmethod
    def treat(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        """Return a modified token"""


class StringFormatter(Formatter):
    """Base class for formatter that only modify the string content"""

    @abc.abstractmethod
    def _treat_string(self, new_string: str) -> str:
        """Will modify the string"""

    def treat(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        return tokenize.TokenInfo(
            tokeninfo.type,
            self._treat_string(tokeninfo.string),
            tokeninfo.start,
            tokeninfo.end,
            tokeninfo.line,
        )


class BeginningQuotesFormatter(StringFormatter):
    """Fix the position of the opening quotes"""

    def _treat_string(self, new_string: str) -> str:
        if new_string[3] == "\n":
            new_string = re.sub(r"\n *", "", new_string, 1)
        return new_string


class ClosingQuotesFormatter(Formatter):
    """Fix the position of the closing quotes"""

    @staticmethod
    def _format_multiline_ending_quotes(
        tokeninfo: tokenize.TokenInfo,
    ) -> tokenize.TokenInfo:
        """Fix the position of end quotes for multi-line docstrings"""
        good_end = f"{(tokeninfo.start[1]) * ' '}{(tokeninfo.string[0]) * 3}"
        new_string = tokeninfo.string
        split_string = new_string.split("\n")

        # Add new line with only quotes
        if not new_string.endswith("\n" + good_end):
            new_string = new_string[:-3] + "\n" + good_end
        # Remove line with only quotes for potential single line string
        elif len(split_string) == 2 and split_string[-1] == good_end:
            new_string = "\n".join(split_string[:-1]) + tokeninfo.string[0] * 3
        return tokenize.TokenInfo(
            tokeninfo.type, new_string, tokeninfo.start, tokeninfo.end, tokeninfo.line
        )

    def treat(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        if "\n" in tokeninfo.string:
            return self._format_multiline_ending_quotes(tokeninfo)
        return tokeninfo


FORMATTERS: List[Formatter] = [
    BeginningQuotesFormatter(),
    ClosingQuotesFormatter(),
]
