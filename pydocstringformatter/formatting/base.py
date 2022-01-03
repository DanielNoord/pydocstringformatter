import abc
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
