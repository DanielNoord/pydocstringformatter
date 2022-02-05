# pylint: disable=too-few-public-methods, protected-access
"""Run class."""

import os
import sys
import tokenize
from pathlib import Path
from typing import List, Union

from pydocstringformatter import __version__, configuration, formatting, utils


class _Run:
    """Main class that represent a run of the program."""

    def __init__(self, argv: Union[List[str], None]) -> None:
        # Load ArgumentsManager and set its namespace as instance's config attribute
        self._arguments_manager = configuration.ArgumentsManager(
            __version__,
            formatting.FORMATTERS,
        )
        self.config = self._arguments_manager.namespace

        if argv := argv or sys.argv[1:]:
            self._arguments_manager.parse_options(argv)
            self._check_files(self.config.files)
        else:
            self._arguments_manager.print_help()

    def _check_files(self, arguments: List[str]) -> None:
        """Find all files and perform the formatting."""
        filepaths = utils._find_python_files(arguments, self.config.exclude)
        self._format_files(filepaths)

    def _format_file(self, filename: Path) -> bool:
        """Format a file."""
        changed_tokens: List[tokenize.TokenInfo] = []
        is_changed = False

        with tokenize.open(filename) as file:
            try:
                tokens = list(tokenize.generate_tokens(file.readline))
            except tokenize.TokenError as exc:
                raise utils.ParsingError(
                    f"Can't parse {os.path.relpath(filename)}. Is it valid Python code?"
                ) from exc

        for index, tokeninfo in enumerate(tokens):
            new_tokeninfo = tokeninfo

            if utils._is_docstring(new_tokeninfo, tokens[index - 1]):
                for formatter in formatting.FORMATTERS:
                    if getattr(self.config, formatter.name):
                        new_tokeninfo = formatter.treat_token(new_tokeninfo)
            changed_tokens.append(new_tokeninfo)

            if tokeninfo != new_tokeninfo:
                is_changed = True

        if is_changed:
            try:
                filename_str = os.path.relpath(filename)
            except ValueError:  # pragma: no cover # Covered on Windows
                # On Windows relpath raises ValueError's when the mounts differ
                filename_str = str(filename)

            if self.config.write:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(tokenize.untokenize(changed_tokens))
                    utils._print_to_console(
                        f"Formatted {filename_str} 📖\n", self.config.quiet
                    )
            else:
                sys.stdout.write(
                    utils._generate_diff(
                        tokenize.untokenize(tokens),
                        tokenize.untokenize(changed_tokens),
                        filename_str,
                    )
                )

        return is_changed

    def _format_files(self, filepaths: List[Path]) -> None:
        """Format a list of files."""
        is_changed = False

        for file in filepaths:
            is_changed = self._format_file(file) or is_changed

        if not is_changed:
            utils._print_to_console(
                "Nothing to do! All docstrings are correct 🎉\n", self.config.quiet
            )
