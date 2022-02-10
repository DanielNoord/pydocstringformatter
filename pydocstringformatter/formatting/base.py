import abc
import re
import tokenize
from typing import Literal


class Formatter:
    """Base class for docstring formatter."""

    optional = False

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the Formatter.

        This will be used to create argparse options when added to
        'pydocstringformatter.formatting.FORMATTERS'. Therefore, it is
        user-facing and should be chosen carefully.
        """

    @property
    def activate_option(self) -> str:
        """The argparse option to activate this formatter."""
        return f"--{self.name}"

    @property
    def deactivate_option(self) -> str:
        """The argparse option to deactivate this formatter."""
        return f"--no-{self.name}"

    @abc.abstractmethod
    def treat_token(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        """Return a modified token."""


class StringFormatter(Formatter):
    """Base class for formatter that only modifies the string content."""

    @abc.abstractmethod
    def _treat_string(self, tokeninfo: tokenize.TokenInfo, indent_length: int) -> str:
        """Return a modified string."""

    def treat_token(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        return tokenize.TokenInfo(
            tokeninfo.type,
            self._treat_string(tokeninfo, tokeninfo.start[1]),
            tokeninfo.start,
            tokeninfo.end,
            tokeninfo.line,
        )


class StringAndQuotesFormatter(Formatter):
    """Base class for string formatter that needs access to the quotes."""

    quotes_regex = re.compile(r"""['"]{1,3}""")
    """Pattern to match against opening quotes."""

    @abc.abstractmethod
    def _treat_string(
        self,
        tokeninfo: tokenize.TokenInfo,
        indent_length: int,
        quotes: str,
        quotes_length: Literal[1, 3],
    ) -> str:
        """Return a modified string."""

    def treat_token(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        # Get the quotes used for this docstring
        match = re.match(self.quotes_regex, tokeninfo.string)
        assert match
        quotes = match.group()

        quotes_length = len(quotes)
        assert quotes_length in {1, 3}

        return tokenize.TokenInfo(
            tokeninfo.type,
            self._treat_string(
                tokeninfo,
                tokeninfo.start[1],
                quotes,
                quotes_length,  # type: ignore[arg-type]
            ),
            tokeninfo.start,
            tokeninfo.end,
            tokeninfo.line,
        )
