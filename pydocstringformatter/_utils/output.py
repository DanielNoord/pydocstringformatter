import sys


def encode_string(string: str) -> bytes:
    """Encode a string to utf-8.

    This can be used to circumvent the issue of the standard encoding
    of a windows console not being utf-8.
    See: https://github.com/DanielNoord/pydocstringformatter/issues/13
    """
    return string.encode("utf-8")


def print_to_console(string: str, quiet: bool) -> None:
    """Print a string to the console while handling edge cases.

    This can be used instead of print() whenever we want to
    print emoji's or non-ASCII characters, but also to check if we are
    in quiet mode.
    """
    if not quiet:
        sys.stdout.buffer.write(encode_string(string))


def sys_exit(value: int, option: bool) -> None:
    """Sys.exit if the boolean passed says to do so."""
    if option:
        sys.exit(value)
