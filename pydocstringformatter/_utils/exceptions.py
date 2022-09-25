class PydocstringFormatterError(Exception):
    """Base class to inherit all exceptions from."""


class ParsingError(PydocstringFormatterError):
    """Raised when we the parsing of a file failed."""


class UnrecognizedOption(PydocstringFormatterError):
    """Raised when an option is encountered that is not recognized."""


class TomlParsingError(PydocstringFormatterError):
    """Raised when there are errors with the parsing of the toml file."""


class UnstableResultError(PydocstringFormatterError):
    """Raised when the result of the formatting is unstable."""
