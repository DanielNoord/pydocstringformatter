import abc
import tokenize


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
