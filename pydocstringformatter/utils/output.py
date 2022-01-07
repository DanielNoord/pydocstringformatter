import sys


def _encode_string(string: str) -> bytes:
    """Encode a string to utf-8.

    This can be used to circumvent the issue of the standard encoding
    of a windows console not being utf-8.
    See: https://github.com/DanielNoord/pydocstringformatter/issues/13
    """
    return string.encode("utf-8")


def _print_to_console(string: str) -> None:
    """Print a string to the console while handling edge cases.

    This should be used instead of print() whenever we want to
    print emoji's or non-ASCII characters.
    """
    sys.stdout.buffer.write(_encode_string(string))
