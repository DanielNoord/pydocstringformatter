from __future__ import annotations

import re
from typing import Literal

from pydocstringformatter._formatting import _utils
from pydocstringformatter._formatting.base import SummaryFormatter


class SplitSummaryAndDocstringFormatter(SummaryFormatter):
    """Split the summary and body of a docstring based on a period and max length.

    The maximum length of a summary can be set with the --max-summary-lines option.
    """

    name = "split-summary-body"

    style = ["pep257"]

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
    def treat_summary(
        self,
        summary: str,
        indent_length: int,
        quotes_length: Literal[1, 3],
        description_exists: bool,
    ) -> str:
        """Split a summary and body if there is a period after the summary."""
        new_summary = None

        if not summary:
            return summary

        if _utils.is_rst_title(summary):
            return summary

        # Try to split on period
        if match := re.search(self.end_of_sentence_period, summary):
            index = match.start()

            if summary[:index].count("\n") < self.config.max_summary_lines:
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
                elif summary[index + 1] == "\n":
                    new_summary = summary[:index] + ".\n\n" + summary[index + 2 :]

        # Try to split on max length
        if not new_summary and summary.count("\n") > self.config.max_summary_lines - 1:
            lines = summary.splitlines()
            new_summary = (
                "\n".join(lines[: self.config.max_summary_lines])
                + "\n\n"
                + "\n".join(lines[self.config.max_summary_lines :])
            )

        return new_summary or summary
