class PydocstringFormatterError(Exception):
    """Base class to inherit all exceptions from"""


class ParsingError(PydocstringFormatterError):
    """Raised when we the parsing of a file failed"""
