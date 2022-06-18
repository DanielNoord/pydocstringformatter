# pylint: disable=too-few-public-methods, protected-access
"""Run class."""
from __future__ import annotations

import os
import sys
import tokenize
from pathlib import Path

from pydocstringformatter import __version__, configuration, formatting, utils


class _Run:
    """Main class that represent a run of the program."""

    def __init__(self, argv: list[str] | None) -> None:
        # Load ArgumentsManager and set its namespace as instance's config attribute
        self._arguments_manager = configuration.ArgumentsManager(
            __version__,
            formatting.FORMATTERS,
        )
        self.config = self._arguments_manager.namespace

        # Display help message if nothing is passed
        if not (argv := argv or sys.argv[1:]):
            self._arguments_manager.print_help()
            return

        # Parse options and register on formatters
        self._arguments_manager.parse_options(argv)
        for formatter in formatting.FORMATTERS:
            formatter.set_config_namespace(self.config)

        self._check_files(self.config.files)

    # pylint: disable-next=inconsistent-return-statements
    def _check_files(self, files: list[str]) -> None:
        """Find all files and perform the formatting."""
        filepaths = utils._find_python_files(files, self.config.exclude)

        is_changed = self._format_files(filepaths)

        if is_changed:  # pylint: disable=consider-using-assignment-expr
            return utils._sys_exit(32, self.config.exit_code)

        files_string = f"{len(filepaths)} "
        files_string += "files" if len(filepaths) != 1 else "file"
        utils._print_to_console(
            f"Nothing to do! All docstrings in {files_string} are correct 🎉\n",
            self.config.quiet,
        )

        utils._sys_exit(0, self.config.exit_code)

    def _format_file(self, filename: Path) -> bool:
        """Format a file."""
        changed_tokens: list[tokenize.TokenInfo] = []
        is_changed = False

        with tokenize.open(filename) as file:
            try:
                tokens = list(tokenize.generate_tokens(file.readline))
            except tokenize.TokenError as exc:
                raise utils.ParsingError(
                    f"Can't parse {os.path.relpath(filename)}. Is it valid Python code?"
                ) from exc
            # Record type of newlines so we can make sure to use
            # the same later on.
            newlines = file.newlines

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
                if isinstance(newlines, tuple):
                    newlines = newlines[0]
                    print(
                        "Found multiple newline variants in "
                        f"{os.path.abspath(filename_str)}. "
                        "Using variant that occurred first.",
                        file=sys.stderr,
                    )
                with open(filename, "w", encoding="utf-8", newline=newlines) as file:
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

    def _format_files(self, filepaths: list[Path]) -> bool:
        """Format a list of files."""
        is_changed = False

        for file in filepaths:
            is_changed = self._format_file(file) or is_changed

        return is_changed
