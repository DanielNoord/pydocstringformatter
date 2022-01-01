# pylint: disable=too-few-public-methods, protected-access
"""Run class"""

import sys
import tokenize
from pathlib import Path
from typing import Union

from pydocstringformatter import formatting, utils


class _Run:
    def __init__(self, argv: Union[list[str], None]) -> None:
        self.arg_parser = utils._register_arguments()

        if argv := argv or sys.argv[1:]:
            self.config = utils._parse_arguments(self.arg_parser, argv)
            self._check_files(self.config.files)
        else:
            self.arg_parser.print_help()

    def _check_files(self, arguments: list[str]) -> None:
        """Find all files and perform the formatting"""
        filepaths = utils._find_python_files(arguments)
        self._format_files(filepaths)

    def _format_file(self, filename: Path) -> None:
        """Format a file"""
        changed_tokens: list[tokenize.TokenInfo] = []

        with tokenize.open(filename) as file:
            tokens = list(tokenize.generate_tokens(file.readline))

        for index, tokeninfo in enumerate(tokens):
            if utils._is_docstring(tokeninfo, tokens[index - 1]):
                if tokeninfo.start[0] != tokeninfo.end[0]:
                    tokeninfo = formatting._format_multiline_quotes(tokeninfo)

            changed_tokens.append(tokeninfo)

        if self.config.write:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(tokenize.untokenize(changed_tokens))
        else:
            sys.stdout.write(tokenize.untokenize(changed_tokens))

    def _format_files(self, filepaths: list[Path]) -> None:
        """Format a list of files"""
        for file in filepaths:
            self._format_file(file)
