from __future__ import annotations

import abc
import argparse
import functools
import re
import tokenize
from typing import Literal


class Formatter:
    """Base class for docstring formatter."""

    optional = False
    config: argparse.Namespace
    """Namespace object set when set_config_namespace is called."""

    style = ["default"]
    """Names of the docstring style(s) that are associated with this formatter.

    Default is always ran.
    """

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

    def set_config_namespace(self, config: argparse.Namespace) -> None:
        """Set the config attribute for this formatter."""
        self.config = config


class StringFormatter(Formatter):
    """Base class for formatter that only modifies the string content."""

    @abc.abstractmethod
    def treat_string(self, tokeninfo: tokenize.TokenInfo, indent_length: int) -> str:
        """Return a modified string."""

    def treat_token(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        return tokenize.TokenInfo(
            tokeninfo.type,
            self.treat_string(tokeninfo, tokeninfo.start[1]),
            tokeninfo.start,
            tokeninfo.end,
            tokeninfo.line,
        )


class StringAndQuotesFormatter(Formatter):
    """Base class for string formatter that needs access to the quotes."""

    quotes_regex = re.compile(r"""['"]{1,3}""")
    """Pattern to match against opening quotes."""

    @abc.abstractmethod
    def treat_string(
        self,
        tokeninfo: tokenize.TokenInfo,
        indent_length: int,
        quotes: str,
        quotes_length: Literal[1, 3],
    ) -> str:
        """Return a modified string."""

    def treat_token(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        # Get the quotes used for this docstring
        match = re.match(self.quotes_regex, tokeninfo.string)
        assert match
        quotes = match.group()

        quotes_length = len(quotes)
        assert quotes_length in {1, 3}

        return tokenize.TokenInfo(
            tokeninfo.type,
            self.treat_string(
                tokeninfo,
                tokeninfo.start[1],
                quotes,
                quotes_length,  # type: ignore[arg-type]
            ),
            tokeninfo.start,
            tokeninfo.end,
            tokeninfo.line,
        )


class SummaryAndDescriptionFormatter(StringAndQuotesFormatter):
    """Base class for formatter that modifies the summary and description."""

    @abc.abstractmethod
    def treat_summary(
        self,
        summary: str,
        indent_length: int,
        quotes_length: Literal[1, 3],
        description_exists: bool,
    ) -> str:
        """Return a modified summary."""

    @abc.abstractmethod
    def treat_description(self, description: str, indent_length: int) -> str:
        """Return a modified description."""

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def separate_summary_and_description(
        docstring: str, indent_length: int, quotes_length: Literal[1, 3]
    ) -> tuple[str, str, str | None]:
        """Split the summary and description and handle quotes and indentation."""
        if "\n\n" in docstring:
            summary, description = docstring.split("\n\n", maxsplit=1)

            # Remove final indentation, ending quotes and new line
            description = description[:-quotes_length]
            if indent_length and description.endswith(indent_length * " "):
                description = description[:-indent_length]
            if description.endswith("\n"):
                description = description[:-1]
        else:
            summary, description = docstring, None

            # Remove final indentation, ending quotes and new line
            summary = summary[:-quotes_length]
            if indent_length and summary.endswith(indent_length * " "):
                summary = summary[:-indent_length]
            if summary.endswith("\n"):
                summary = summary[:-1]

        # Remove opening quotes
        summary = summary[quotes_length:]

        # Prefix is the new-line + indentation for summaries that
        # are not on the same line as the opening quotes
        prefix = ""
        if summary.startswith("\n"):
            prefix = "\n" + indent_length * " "
            summary = summary[1 + indent_length :]
        return prefix, summary, description

    def treat_string(
        self,
        tokeninfo: tokenize.TokenInfo,
        indent_length: int,
        quotes: str,
        quotes_length: Literal[1, 3],
    ) -> str:
        prefix, summary, description = self.separate_summary_and_description(
            tokeninfo.string,
            indent_length,
            quotes_length,
        )

        new_summary = self.treat_summary(
            summary, indent_length, quotes_length, bool(description)
        )
        docstring = f"{quotes}{prefix}{new_summary}"

        if description:
            new_description = self.treat_description(description, indent_length)
            docstring += f"\n\n{new_description}"

        # Determine whether ending quotes were initially on same or new line
        if tokeninfo.string.splitlines()[-1] == indent_length * " " + quotes:
            return f"{docstring}\n{indent_length * ' '}{quotes}"
        return f"{docstring}{quotes}"


class SummaryFormatter(SummaryAndDescriptionFormatter):
    """Base class for formatter that only modifies the summary of a docstring."""

    @abc.abstractmethod
    def treat_summary(
        self,
        summary: str,
        indent_length: int,
        quotes_length: Literal[1, 3],
        description_exists: bool,
    ) -> str:
        """Return a modified summary."""

    def treat_description(self, description: str, indent_length: int) -> str:
        return description
