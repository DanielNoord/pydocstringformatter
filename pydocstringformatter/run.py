# pylint: disable=too-few-public-methods, protected-access
"""Run class."""
from __future__ import annotations

import os
import sys
import tokenize
from pathlib import Path

from pydocstringformatter import __version__, _formatting, _utils
from pydocstringformatter._configuration.arguments_manager import ArgumentsManager
from pydocstringformatter._utils.exceptions import UnstableResultError


class _Run:
    """Main class that represent a run of the program."""

    def __init__(self, argv: list[str] | None) -> None:
        # Load ArgumentsManager and set its namespace as instance's config attribute
        self._arguments_manager = ArgumentsManager(__version__, _formatting.FORMATTERS)
        self.config = self._arguments_manager.namespace

        # Display help message if nothing is passed
        if not (argv := argv or sys.argv[1:]):
            self._arguments_manager.print_help()
            return

        # Parse options and register on formatters
        self._arguments_manager.parse_options(argv)
        for formatter in _formatting.FORMATTERS:
            formatter.set_config_namespace(self.config)

        self.enabled_formatters = self.get_enabled_formatters()
        self.check_files(self.config.files)

    # pylint: disable-next=inconsistent-return-statements
    def check_files(self, files: list[str]) -> None:
        """Find all files and perform the formatting."""
        filepaths = _utils.find_python_files(files, self.config.exclude)

        is_changed = self.format_files(filepaths)

        if is_changed:  # pylint: disable=consider-using-assignment-expr
            return _utils.sys_exit(32, self.config.exit_code)

        files_string = f"{len(filepaths)} "
        files_string += "files" if len(filepaths) != 1 else "file"
        _utils.print_to_console(
            f"Nothing to do! All docstrings in {files_string} are correct 🎉\n",
            self.config.quiet,
        )

        _utils.sys_exit(0, self.config.exit_code)

    def format_file(self, filename: Path) -> bool:
        """Format a file."""
        with tokenize.open(filename) as file:
            try:
                tokens = list(tokenize.generate_tokens(file.readline))
            except tokenize.TokenError as exc:
                raise _utils.ParsingError(
                    f"Can't parse {os.path.relpath(filename)}. Is it valid Python code?"
                ) from exc
            # Record type of newlines so we can make sure to use
            # the same later on.
            newlines = file.newlines

        formatted_tokens, is_changed = self.format_file_tokens(tokens, filename)

        if is_changed:
            try:
                filename_str = os.path.relpath(filename)
            except ValueError:
                # On Windows relpath raises ValueError's when the mounts differ
                filename_str = str(filename)

            if self.config.write:
                if isinstance(newlines, tuple):
                    newlines = newlines[0]
                    print(
                        "Found multiple newline variants in "
                        f"{os.path.abspath(filename_str)}. "
                        "Using variant that occurred first.",
                        file=sys.stderr,
                    )
                with open(filename, "w", encoding="utf-8", newline=newlines) as file:
                    file.write(tokenize.untokenize(formatted_tokens))
                    _utils.print_to_console(
                        f"Formatted {filename_str} 📖\n", self.config.quiet
                    )
            else:
                sys.stdout.write(
                    _utils.generate_diff(
                        tokenize.untokenize(tokens),
                        tokenize.untokenize(formatted_tokens),
                        filename_str,
                    )
                )

        return is_changed

    def get_enabled_formatters(self) -> dict[str, _formatting.Formatter]:
        """Returns a dict of the enabled formatters."""

        enabled = {}
        for formatter in _formatting.FORMATTERS:
            if (
                "default" in formatter.style
                or any(i in formatter.style for i in self.config.style)
            ) and getattr(self.config, formatter.name):
                enabled[formatter.name] = formatter

        return enabled

    def format_file_tokens(
        self, tokens: list[tokenize.TokenInfo], filename: Path
    ) -> tuple[list[tokenize.TokenInfo], bool]:
        """Format a list of tokens.

        tokens: List of tokens to format.
        filename: Name of the file the tokens are from.

        Returns:
            A tuple containing [1] the formatted tokens in a list
            and [2] a boolean indicating if the tokens were changed.

        Raises:
            UnstableResultError::
                If the formatters are not able to get to a stable result.
                It reports what formatters are still modifying the tokens.
        """
        formatted_tokens: list[tokenize.TokenInfo] = []
        is_changed = False

        for index, tokeninfo in enumerate(tokens):
            new_tokeninfo = tokeninfo

            if _utils.is_docstring(new_tokeninfo, tokens[index - 1]):
                new_tokeninfo, changers = self.apply_formatters(new_tokeninfo)
                is_changed = is_changed or bool(changers)

                # Run formatters again (3rd time) to check if the result is stable
                _, changers = self._apply_formatters_once(
                    new_tokeninfo,
                )

                if changers:
                    conflicting_formatters = {
                        k: v
                        for k, v in self.enabled_formatters.items()
                        if k in changers
                    }
                    template = _utils.create_gh_issue_template(
                        new_tokeninfo, conflicting_formatters, str(filename)
                    )

                    raise UnstableResultError(template)

            formatted_tokens.append(new_tokeninfo)

        return formatted_tokens, is_changed

    def apply_formatters(
        self, token: tokenize.TokenInfo
    ) -> tuple[tokenize.TokenInfo, set[str]]:
        """Apply the formatters twice to a token.

        Also tracks which formatters changed the token.

        Returns:
            A tuple containing:
            [1] the formatted token and
            [2] a set of formatters that changed the token.
        """
        token, changers = self._apply_formatters_once(token)
        if changers:
            token, changers2 = self._apply_formatters_once(token)
            changers.update(changers2)
        return token, changers

    def _apply_formatters_once(
        self, token: tokenize.TokenInfo
    ) -> tuple[tokenize.TokenInfo, set[str]]:
        """Applies formatters to a token and keeps track of what changes it.

        token: Token to apply formatters to

        Returns:
            A tuple containing [1] the formatted token and [2] a set
            of formatters that changed the token.
        """
        changers: set[str] = set()
        for formatter_name, formatter in self.enabled_formatters.items():
            if (new_token := formatter.treat_token(token)) != token:
                changers.add(formatter_name)
                token = new_token

        return token, changers

    def format_files(self, filepaths: list[Path]) -> bool:
        """Format a list of files."""
        is_changed = [self.format_file(file) for file in filepaths]
        return any(is_changed)
