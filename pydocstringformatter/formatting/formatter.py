import abc
import re
import tokenize


class Formatter:
    """Base class for docstring formatter"""

    @abc.abstractmethod
    def treat_token(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        """Return a modified token"""


class StringFormatter(Formatter):
    """Base class for formatter that only modifies the string content"""

    @abc.abstractmethod
    def _treat_string(self, tokeninfo: tokenize.TokenInfo) -> str:
        """Return a modified string"""

    def treat_token(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        return tokenize.TokenInfo(
            tokeninfo.type,
            self._treat_string(tokeninfo),
            tokeninfo.start,
            tokeninfo.end,
            tokeninfo.line,
        )


class BeginningQuotesFormatter(StringFormatter):
    """Fix the position of the opening quotes"""

    def _treat_string(self, tokeninfo: tokenize.TokenInfo) -> str:
        new_string = tokeninfo.string
        if new_string[3] == "\n":
            new_string = re.sub(r"\n *", "", new_string, 1)
        return new_string


class ClosingQuotesFormatter(StringFormatter):
    """Fix the position of the closing quotes"""

    def _treat_string(self, tokeninfo: tokenize.TokenInfo) -> str:
        """Fix the position of end quotes for multi-line docstrings"""
        new_string = tokeninfo.string
        if "\n" not in new_string:
            # Not a multiline docstring, nothing to do
            return new_string
        good_end = f"{(tokeninfo.start[1]) * ' '}{(new_string[0]) * 3}"
        split_string = new_string.split("\n")

        # Add new line with only quotes
        if not new_string.endswith("\n" + good_end):
            new_string = new_string[:-3] + "\n" + good_end
        # Remove line with only quotes for potential single line string
        elif len(split_string) == 2 and split_string[-1] == good_end:
            new_string = "\n".join(split_string[:-1]) + tokeninfo.string[0] * 3
        return new_string
