import re
import tokenize

from pydocstringformatter.formatting.base import StringFormatter


class BeginningQuotesFormatter(StringFormatter):
    """Fix the position of the opening quotes"""

    name = "beginning-quotes"

    def _treat_string(self, tokeninfo: tokenize.TokenInfo) -> str:
        new_string = tokeninfo.string
        if new_string[3] == "\n":
            new_string = re.sub(r"\n *", "", new_string, 1)
        return new_string


class ClosingQuotesFormatter(StringFormatter):
    """Fix the position of the closing quotes"""

    name = "closing-quotes"

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


class FinalPeriodFormatter(StringFormatter):
    """Add a period to the end of single line docstrings and summaries."""

    name = "final-period"

    def _treat_string(self, tokeninfo: tokenize.TokenInfo) -> str:
        """Add a period to the end of single-line docstrings and summaries."""
        # Handle single line docstrings
        if not tokeninfo.string.count("\n"):
            if tokeninfo.string[-4] != ".":
                return tokeninfo.string[:-3] + "." + tokeninfo.string[-3:]
        # Handle multi-line docstrings
        else:
            first_linebreak = tokeninfo.string.index("\n")
            # If first linebreak is followed by another we're dealing with a summary
            if tokeninfo.string[tokeninfo.string.index("\n") + 1] == "\n":
                if tokeninfo.string[first_linebreak - 1] != ".":
                    return (
                        tokeninfo.string[:first_linebreak]
                        + "."
                        + tokeninfo.string[first_linebreak:]
                    )
            # pylint: disable=fixme
            # TODO: Handle multi-line docstrings that do not have a summary
            # This is obviously dependent on whether 'pydocstringformatter' will
            # start enforcing summaries :)
        return tokeninfo.string
