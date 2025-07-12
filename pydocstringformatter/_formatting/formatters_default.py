from __future__ import annotations

import re
import textwrap
import tokenize
from typing import Literal

from pydocstringformatter._formatting import _utils
from pydocstringformatter._formatting.base import (
    StringAndQuotesFormatter,
    StringFormatter,
    SummaryFormatter,
)


class BeginningQuotesFormatter(StringFormatter):
    """Fix the position of the opening quotes."""

    name = "beginning-quotes"
    potential_single_line = re.compile(
        r"""
        ['"]{1,3}         # 3 opening quotes
        \n\s*.+           # A line with any length of characters
        \n\s*             # A line with only whitespace
        ['"]{1,3}         # 3 ending quote
    """,
        re.X,
    )
    """Regex pattern to match against a potential single line docstring."""

    def treat_string(self, tokeninfo: tokenize.TokenInfo, _: int) -> str:
        new_string = tokeninfo.string
        if new_string[3] == "\n":
            if (
                new_string.count("\n") == 1  # Single line docstring
                or self.config.summary_quotes_same_line  # Config for multi-line
                or self.potential_single_line.match(new_string)  # Potential single line
            ):
                new_string = re.sub(r"\n *", "", new_string, count=1)
        return new_string


class CapitalizeFirstLetterFormatter(StringFormatter):
    """Capitalize the first letter of the docstring if appropriate."""

    name = "capitalize-first-letter"
    first_letter_re = re.compile(
        StringAndQuotesFormatter.quotes_regex.pattern + r"""\s*(\w)""", re.DOTALL
    )

    def treat_string(self, tokeninfo: tokenize.TokenInfo, _: int) -> str:
        new_string = None
        if match := self.first_letter_re.match(tokeninfo.string):
            first_letter = match.end() - 1
            new_string = (
                tokeninfo.string[:first_letter]
                + tokeninfo.string[first_letter].upper()
                + tokeninfo.string[first_letter + 1 :]
            )
        return new_string or tokeninfo.string


class LineWrapperFormatter(SummaryFormatter):
    """Linewrap the docstring by the pre-defined line length."""

    name = "linewrap-full-docstring"
    optional = True

    def treat_summary(
        self,
        summary: str,
        indent_length: int,
        quotes_length: Literal[1, 3],
        description_exists: bool,
    ) -> str:
        """Wrap the summary of a docstring."""

        line_length = self.config.max_line_length

        # Without a description we need to consider the length including closing quotes
        if not description_exists:
            # Calculate length without the ending quotes
            length_without_ending = indent_length + quotes_length + len(summary)

            # If potential length is less than line length we need to consider ending
            # quotes as well for the line length
            if length_without_ending < line_length:
                # We subtract one more because we don't want a new line with just the
                # ending quotes
                line_length -= quotes_length + 1

        if not (summary_lines := summary.splitlines()):
            summary_lines = [""]

        new_summary = "\n".join(
            textwrap.wrap(
                summary_lines[0],
                width=line_length,
                initial_indent=" " * (indent_length + quotes_length),
                subsequent_indent=" " * indent_length,
                replace_whitespace=True,
            )
        )[indent_length + quotes_length :]

        if len(summary_lines) > 1:
            for line in summary_lines[1:]:
                new_summary += "\n"
                new_summary += "\n".join(
                    textwrap.wrap(
                        line,
                        width=line_length,
                        subsequent_indent=" " * indent_length,
                        replace_whitespace=True,
                    )
                )

        return new_summary


class ClosingQuotesFormatter(StringFormatter):
    """Fix the position of the closing quotes."""

    name = "closing-quotes"

    def treat_string(self, tokeninfo: tokenize.TokenInfo, _: int) -> str:
        """Fix the position of end quotes for multi-line docstrings."""
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


class FinalPeriodFormatter(SummaryFormatter):
    """Add a period to the end of single line docstrings and summaries."""

    name = "final-period"
    END_OF_SENTENCE_PUNCTUATION = {".", "?", "!", "‽", ":", ";"}

    def treat_summary(
        self,
        summary: str,
        indent_length: int,
        quotes_length: Literal[1, 3],
        description_exists: bool,
    ) -> str:
        """Add a period to the end of single-line docstrings and summaries."""
        if not summary:
            return summary

        if summary[-1] in self.END_OF_SENTENCE_PUNCTUATION:
            return summary

        if _utils.is_rst_title(summary):
            return summary

        return summary + "."


class StripWhitespacesFormatter(StringAndQuotesFormatter):
    """Strip 1) docstring start, 2) docstring end and 3) end of line."""

    name = "strip-whitespaces"

    def treat_string(
        self,
        tokeninfo: tokenize.TokenInfo,
        indent_length: int,
        quotes: str,
        quotes_length: Literal[1, 3],
    ) -> str:
        """Strip whitespaces."""
        lines = tokeninfo.string[quotes_length:-quotes_length].split("\n")
        new_lines: list[str] = []

        for index, line in enumerate(lines):
            if line == "":
                # Remove double white lines
                if index and lines[index - 1] == "":
                    continue

            # On the first line strip from both sides
            if index == 0:  # pylint: disable=compare-to-zero
                new_lines.append(line.lstrip().rstrip())

            # Check last line
            elif index == len(lines) - 1:
                # If completely whitespace, just return the indent_length
                if line.count(" ") == len(line):
                    new_lines.append(indent_length * " ")
                else:
                    new_lines.append(line)

            # Else, only strip right side
            else:
                new_lines.append(line.rstrip())

        # Remove a final white line
        if len(new_lines) > 3 and new_lines[-2] == "":
            new_lines.pop(-2)

        return quotes + "\n".join(new_lines) + quotes


class QuotesTypeFormatter(StringAndQuotesFormatter):
    """Change all opening and closing quotes to be triple quotes."""

    name = "quotes-type"

    def treat_string(
        self,
        tokeninfo: tokenize.TokenInfo,
        _: int,
        __: str,
        quotes_length: Literal[1, 3],
    ) -> str:
        """Change all opening and closing quotes if necessary."""
        return f'"""{tokeninfo.string[quotes_length:-quotes_length]}"""'
