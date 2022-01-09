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
    def _treat_string(self, tokeninfo: tokenize.TokenInfo) -> str:
        """Return a modified string."""

    def treat_token(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        return tokenize.TokenInfo(
            tokeninfo.type,
            self._treat_string(tokeninfo),
            tokeninfo.start,
            tokeninfo.end,
            tokeninfo.line,
        )
