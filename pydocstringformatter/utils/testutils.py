import contextlib
import logging
from pathlib import Path
from types import TracebackType
from typing import List, Type, Union

import pytest

import pydocstringformatter
from pydocstringformatter.formatting import Formatter

LOGGER = logging.getLogger(__name__)


class FormatterAssert(contextlib.AbstractContextManager):  # type: ignore[type-arg]

    """Permit to assert that a Formatter does something on a docstring.

    Also permit to check that nothing happen if it's deactivated.
    """

    def __init__(
        self,
        docstring: str,
        formatters: List[Formatter],
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path,
    ):
        self.formatters = formatters
        file_name = "_".join([f.name for f in self.formatters])
        self.file_to_format = tmp_path / f"test_{file_name}.py"
        self.file_to_format.write_text(docstring)
        self.capsys = capsys
        names = [f"'{f.name}'" for f in formatters]
        verb = "is" if len(names) == 1 else "are"
        self.assert_msg = f"""
{{}} was modified but {', '.join(names)} {verb} {{}}.
Temp file is '{self.file_to_format}'
"""

    def __enter__(self) -> "FormatterAssert":
        return self

    @staticmethod
    def __launch(commands: List[str]) -> None:
        """Launch pydocstringformatter, with a logging for easier debug."""
        pydocstringformatter.run_docstring_formatter(commands)
        LOGGER.info("Launching 'pydocstringformatter' with: %s", commands)

    def assert_format_when_activated(self) -> None:
        """The formatter does something when activated."""
        msg = self.assert_msg.format("Nothing", "activated")
        self.__launch(
            [str(self.file_to_format)] + [f.activate_option for f in self.formatters]
        )
        out, err = self.capsys.readouterr()
        assert not err
        assert "Nothing to do!" not in out, msg
        expected = ["---", "@@", "+++"]
        assert all(e in out for e in expected), msg

    def assert_no_change_when_deactivated(self) -> None:
        """The formatter does nothing when deactivated."""
        self.__launch(
            [str(self.file_to_format)] + [f.deactivate_option for f in self.formatters]
        )
        out, err = self.capsys.readouterr()
        assert not err
        assert "Nothing to do!" in out, self.assert_msg.format(
            "Something", "deactivated"
        )

    def __exit__(
        self,
        exc_type: Union[Type[BaseException], None],
        exc_val: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ) -> None:
        return None
