# pylint: disable = redefined-outer-name
import os
import sys
from pathlib import Path

import pytest

import pydocstringformatter
from pydocstringformatter._formatting import FORMATTERS
from pydocstringformatter._formatting.base import StringFormatter
from pydocstringformatter._formatting.formatters_pep257 import (
    SplitSummaryAndDocstringFormatter,
)
from pydocstringformatter._testutils import FormatterAsserter


def test_no_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that we display a help message when no arguments are provided."""
    sys.argv = ["pydocstringformatter"]
    pydocstringformatter.run_docstring_formatter()
    out, err = capsys.readouterr()
    assert out.startswith("usage: pydocstringformatter [-h]")

    # Test that we print help messages for individual formatters as well
    # Default formatter
    assert "--strip-whitespaces" in out
    assert "Activate or deactivate strip-whitespaces" in out
    # Optional formatter
    assert "--split-summary-body" in out
    assert "Activate or deactivate split-summary-body" in out
    assert not err


def test_formatter_help_categories(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that formatter messages are in the correct group."""

    class OptionalFormatter(StringFormatter):  # pylint: disable=abstract-method
        """An optional formatter."""

        name = "optional-formatter"
        optional = True

    class NonOptionalFormatter(StringFormatter):  # pylint: disable=abstract-method
        """A non-optional formatter."""

        name = "non-optional-formatter"

    FORMATTERS.append(OptionalFormatter())  # type: ignore[abstract]
    FORMATTERS.append(NonOptionalFormatter())  # type: ignore[abstract]
    sys.argv = ["pydocstringformatter"]
    pydocstringformatter.run_docstring_formatter()
    out, _ = capsys.readouterr()
    categories = out.replace("\n\n ", "\n").split("\n\n")
    for category in categories:
        if category.startswith("optional formatters"):
            assert "--optional-formatter" in category
            assert "--non-optional-formatter" not in category
        elif category.startswith("default formatters"):
            assert "--optional-formatter" not in category
            assert "--non-optional-formatter" in category
    FORMATTERS.pop()
    FORMATTERS.pop()


def test_sys_agv_as_arguments(
    capsys: pytest.CaptureFixture[str], test_file: str
) -> None:
    """Test running with arguments in sys.argv."""
    sys.argv = ["pydocstringformatter", test_file]
    pydocstringformatter.run_docstring_formatter()

    with open(test_file, encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring."""'

    output = capsys.readouterr()
    assert output.out.endswith(
        '''
@@ -1,2 +1,4 @@
-"""A multi-line
-docstring."""
+"""A multi-line.
+
+docstring.
+"""
'''
    )
    assert not output.err


def test_output_message_nothing_done(
    capsys: pytest.CaptureFixture[str], test_file: str
) -> None:
    """Test that we emit the correct message when nothing was done."""
    with open(test_file, "w", encoding="utf-8") as file:
        file.write('"""A multi-line.\n\ndocstring.\n"""')
    with open(test_file.replace(".py", "2.py"), "w", encoding="utf-8") as file:
        file.write('"""A multi-line.\n\ndocstring.\n"""')

    pydocstringformatter.run_docstring_formatter(
        [str(Path(test_file).parent), "--write"]
    )

    output = capsys.readouterr()
    assert output.out == "Nothing to do! All docstrings in 2 files are correct 🎉\n"
    assert not output.err


def test_output_message_one_file(
    capsys: pytest.CaptureFixture[str], test_file: str
) -> None:
    """Test that we emit the correct message when one out of two files was formatted."""
    try:
        expected_path = os.path.relpath(test_file)
    except ValueError:
        expected_path = test_file

    with open(test_file.replace(".py", "2.py"), "w", encoding="utf-8") as file:
        file.write('"""A multi-line.\n\ndocstring.\n"""')

    pydocstringformatter.run_docstring_formatter(
        [str(Path(test_file).parent), "--write"]
    )

    output = capsys.readouterr()
    assert output.out == f"Formatted {expected_path} 📖\n"
    assert not output.err


def test_output_message_two_files(
    capsys: pytest.CaptureFixture[str], test_file: str
) -> None:
    """Test that we emit the correct message when two files were formatted."""
    second_file = test_file.replace(".py", "2.py")

    try:
        expected_path = os.path.relpath(test_file)
        expected_second_path = os.path.relpath(second_file)
    except ValueError:
        expected_path = test_file
        expected_second_path = second_file

    with open(second_file, "w", encoding="utf-8") as file:
        file.write('"""A multi-line\ndocstring"""')

    pydocstringformatter.run_docstring_formatter(
        [str(Path(test_file).parent), "--write"]
    )

    output = capsys.readouterr()
    assert (
        output.out
        == f"""Formatted {expected_path} 📖
Formatted {expected_second_path} 📖
"""
    )
    assert not output.err


def test_begin_quote_formatters(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    """Test that (optional) formatters are activated or not depending on options."""
    with FormatterAsserter(
        f'"""{"a" * 120}\n{"b" * 120}"""', FORMATTERS, capsys, tmp_path
    ) as asserter:
        asserter.assert_format_when_activated()
        asserter.assert_no_change_when_deactivated()


def test_optional_formatters_argument(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    """Test that an optional formatter is correctly turned on and off with arguments."""
    with FormatterAsserter(
        '"""Summary. Body."""', [SplitSummaryAndDocstringFormatter()], capsys, tmp_path
    ) as asserter:
        asserter.assert_format_when_activated()
        asserter.assert_no_change_when_deactivated()


class TestExitCodes:
    """Tests for the --exit-code option."""

    @staticmethod
    def test_exit_code_with_write(test_file: str) -> None:
        """Test that we emit the correct exit code in write mode."""
        with pytest.raises(SystemExit) as exit_exec:
            pydocstringformatter.run_docstring_formatter(
                [str(Path(test_file)), "--write", "--exit-code"]
            )

        assert exit_exec.value.code == 32

        # After first writing changes, now we expect no changes
        with pytest.raises(SystemExit) as exit_exec:
            pydocstringformatter.run_docstring_formatter(
                [str(Path(test_file)), "--write", "--exit-code"]
            )

        assert not exit_exec.value.code

    @staticmethod
    def test_exit_code_without_write(test_file: str) -> None:
        """Test that we emit the correct exit code in write mode."""
        with pytest.raises(SystemExit) as exit_exec:
            pydocstringformatter.run_docstring_formatter(
                [str(Path(test_file)), "--exit-code"]
            )

        assert exit_exec.value.code == 32

        # We expect an exit code on both occassions
        with pytest.raises(SystemExit) as exit_exec:
            pydocstringformatter.run_docstring_formatter(
                [str(Path(test_file)), "--exit-code"]
            )

        assert exit_exec.value.code == 32
