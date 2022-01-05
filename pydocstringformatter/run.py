# pylint: disable=too-few-public-methods, protected-access
"""Run class"""

import argparse
import os
import sys
import tokenize
from pathlib import Path
from typing import List, Union

from pydocstringformatter import __version__, formatting, utils


class _Run:
    """Main class that represent a run of the program"""

    def __init__(self, argv: Union[List[str], None]) -> None:
        # Needed to display emoji's on Windows. Mypy doesn't recognize
        # this because stdout isn't inferred as io.TextIOWrapper
        # See https://github.com/DanielNoord/pydocstringformatter/issues/13
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]

        self.arg_parser = utils._register_arguments(__version__)
        self.config = argparse.Namespace()

        if argv := argv or sys.argv[1:]:
            utils._parse_toml_file(self.arg_parser, self.config)
            utils._parse_command_line_arguments(self.arg_parser, argv, self.config)

            self._check_files(self.config.files)
        else:
            self.arg_parser.print_help()

    def _check_files(self, arguments: List[str]) -> None:
        """Find all files and perform the formatting"""
        filepaths = utils._find_python_files(arguments)
        self._format_files(filepaths)

    def _format_file(self, filename: Path) -> bool:
        """Format a file"""
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
                    new_tokeninfo = formatter.treat_token(new_tokeninfo)
            changed_tokens.append(new_tokeninfo)

            if tokeninfo != new_tokeninfo:
                is_changed = True

        if is_changed:
            if self.config.write:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(tokenize.untokenize(changed_tokens))
                try:
                    utils._print_to_console(
                        f"Formatted {os.path.relpath(filename)} 📖\n"
                    )
                except ValueError:  # pragma: no cover
                    # On Windows relpath raises ValueError's when mounts differ
                    utils._print_to_console(f"Formatted {filename} 📖\n")
            else:
                sys.stdout.write(tokenize.untokenize(changed_tokens))

        return is_changed

    def _format_files(self, filepaths: List[Path]) -> None:
        """Format a list of files"""
        is_changed = False

        for file in filepaths:
            is_changed = self._format_file(file) or is_changed

        if not is_changed:
            utils._print_to_console("Nothing to do! All docstrings are correct 🎉\n")
