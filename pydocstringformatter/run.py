# pylint: disable=too-few-public-methods, protected-access
"""Run class"""

import sys
import tokenize
from pathlib import Path
from typing import List, Union

from pydocstringformatter import __version__, formatting, utils


class _Run:
    """Main class that represent a run of the program"""

    def __init__(self, argv: Union[List[str], None]) -> None:
        self.arg_parser = utils._register_arguments(__version__)

        if argv := argv or sys.argv[1:]:
            self.config = utils._parse_arguments(self.arg_parser, argv)
            self._check_files(self.config.files)
        else:
            self.arg_parser.print_help()

    def _check_files(self, arguments: List[str]) -> None:
        """Find all files and perform the formatting"""
        filepaths = utils._find_python_files(arguments)
        self._format_files(filepaths)

    def _format_file(self, filename: Path) -> None:
        """Format a file"""
        changed_tokens: List[tokenize.TokenInfo] = []

        with tokenize.open(filename) as file:
            tokens = list(tokenize.generate_tokens(file.readline))

        for index, tokeninfo in enumerate(tokens):
            if utils._is_docstring(tokeninfo, tokens[index - 1]):
                tokeninfo = formatting._format_beginning_quotes(tokeninfo)

                if "\n" in tokeninfo.string:
                    tokeninfo = formatting._format_multiline_quotes(tokeninfo)

            changed_tokens.append(tokeninfo)

        if self.config.write:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(tokenize.untokenize(changed_tokens))
        else:
            sys.stdout.write(tokenize.untokenize(changed_tokens))

    def _format_files(self, filepaths: List[Path]) -> None:
        """Format a list of files"""
        for file in filepaths:
            self._format_file(file)
