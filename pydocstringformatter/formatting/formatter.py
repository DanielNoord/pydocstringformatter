import re
import tokenize
from typing import Literal

from pydocstringformatter.formatting.base import (
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

    def _treat_string(self, tokeninfo: tokenize.TokenInfo, _: int) -> str:
        new_string = tokeninfo.string
        if new_string[3] == "\n":
            if (
                new_string.count("\n") == 1  # Single line docstring
                or self.config.summary_quotes_same_line  # Config for multi-line
                or self.potential_single_line.match(new_string)  # Potential single line
            ):
                new_string = re.sub(r"\n *", "", new_string, 1)
        return new_string


class CapitalizeFirstLetterFormatter(StringFormatter):
    """Capitalize the first letter of the docstring if appropriate."""

    name = "capitalize-first-letter"
    first_letter_re = re.compile(r"""['"]{1,3}\s*(\w)""", re.DOTALL)

    def _treat_string(self, tokeninfo: tokenize.TokenInfo, _: int) -> str:
        new_string = None
        if match := self.first_letter_re.match(tokeninfo.string):
            first_letter = match.end() - 1
            new_string = (
                tokeninfo.string[:first_letter]
                + tokeninfo.string[first_letter].upper()
                + tokeninfo.string[first_letter + 1 :]
            )
        return new_string or tokeninfo.string


class ClosingQuotesFormatter(StringFormatter):
    """Fix the position of the closing quotes."""

    name = "closing-quotes"

    def _treat_string(self, tokeninfo: tokenize.TokenInfo, _: int) -> str:
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


class FinalPeriodFormatter(StringAndQuotesFormatter):
    """Add a period to the end of single line docstrings and summaries."""

    name = "final-period"
    END_OF_SENTENCE_PUNCTUATION = {".", "?", "!", "‽", ":", ";"}

    def _treat_string(
        self,
        tokeninfo: tokenize.TokenInfo,
        _: int,
        quotes: str,
        quotes_length: Literal[1, 3],
    ) -> str:
        """Add a period to the end of single-line docstrings and summaries."""
        # Handle single line docstrings
        if not tokeninfo.string.count("\n"):
            if (
                tokeninfo.string[-quotes_length - 1]
                not in self.END_OF_SENTENCE_PUNCTUATION
            ):
                return tokeninfo.string[:-quotes_length] + "." + quotes
        # Handle multi-line docstrings
        else:
            lines = tokeninfo.string.splitlines()
            # If second line is one recurring character we're dealing with a rst title
            if (stripped := lines[1].lstrip()) and stripped.count(stripped[0]) == len(
                stripped
            ):
                return tokeninfo.string
            # If second line is empty we're dealing with a summary
            if lines[1] == "":
                if lines[0][-1] not in self.END_OF_SENTENCE_PUNCTUATION:
                    return lines[0] + ".\n" + "\n".join(lines[1:])
            # TODO(#26): Handle multi-line docstrings that do not have a summary
            # This is obviously dependent on whether 'pydocstringformatter' will
            # start enforcing summaries :)
        return tokeninfo.string


class SplitSummaryAndDocstringFormatter(SummaryFormatter):
    """Split the summary and body of a docstring based on a period and max length.

    The maximum length of a summary can be set with the --max-summary-lines option.

    This formatter is currently optional as its considered somwehat opinionated
    and might require major refactoring for existing projects.
    """

    name = "split-summary-body"
    # TODO(#68): Make this non-optional
    optional = True

    end_of_sentence_period = re.compile(
        r"""
        (?<!e.g|i.e|etc)                        # Not preceded by 'e.g', 'i.e', 'etc'
        \.                                  # A dot
        (?!\w)                              # Not followed by a letter
        """,
        re.X,
    )
    """Pattern to match against an end of sentence period."""

    # pylint: disable-next=too-many-branches
    def _treat_summary(self, summary: str, indent_length: int) -> str:
        """Split a summary and body if there is a period after the summary."""
        new_summary = None

        # Try to split on period
        if match := re.search(self.end_of_sentence_period, summary):
            index = match.start()

            if summary[: index - 1].count("\n") < self.config.max_summary_lines:
                if len(summary) == index + 1:
                    new_summary = summary

                # Handle summaries with more text on same line after the period
                elif summary[index + 1] == " ":
                    new_summary = (
                        summary[:index]
                        + f"\n\n{' ' * indent_length}"
                        + summary[index + 2 :]
                    )

                # Handle summaries that end with a period and a direct new line
                # but not a double new line.
                elif summary[index + 1] == "\n":
                    # If this is the end of the docstring, don't do anything
                    if summary[index + 2 :] == indent_length * " ":
                        new_summary = summary
                    # Split between period and rest of docstring
                    else:
                        new_summary = summary[:index] + ".\n\n" + summary[index + 2 :]

        # Try to split on max length
        if not new_summary and summary.count("\n") > self.config.max_summary_lines - 1:
            lines = summary.splitlines()
            new_summary = "\n".join(lines[: self.config.max_summary_lines])

            # Handle summaries without any additional text beyond max lines
            if lines[self.config.max_summary_lines] == indent_length * " ":
                new_summary += "\n" + lines[self.config.max_summary_lines]

            # Split between max lines and rest of docstring
            else:
                new_summary += "\n\n" + "\n".join(
                    lines[self.config.max_summary_lines :]
                )

        return new_summary or summary


class StripWhitespacesFormatter(StringAndQuotesFormatter):
    """Strip 1) docstring start, 2) docstring end and 3) end of line."""

    name = "strip-whitespaces"

    def _treat_string(
        self,
        tokeninfo: tokenize.TokenInfo,
        indent_length: int,
        quotes: str,
        quotes_length: Literal[1, 3],
    ) -> str:
        """Strip whitespaces."""
        lines = tokeninfo.string[quotes_length:-quotes_length].split("\n")
        for index, line in enumerate(lines):
            if index == 0:  # pylint: disable=compare-to-zero
                lines[index] = line.lstrip().rstrip()
            elif index == len(lines) - 1:
                # Remove whitespaces if last line is completely empty
                if len(line) > indent_length and line.count(" ") == len(line):
                    lines[index] = ""
            else:
                lines[index] = line.rstrip()

        return quotes + "\n".join(lines) + quotes


class QuotesTypeFormatter(StringAndQuotesFormatter):
    """Change all opening and closing quotes to be triple quotes."""

    name = "quotes-type"

    def _treat_string(
        self,
        tokeninfo: tokenize.TokenInfo,
        _: int,
        __: str,
        quotes_length: Literal[1, 3],
    ) -> str:
        """Change all opening and closing quotes if necessary."""
        return f'"""{tokeninfo.string[quotes_length:-quotes_length]}"""'
