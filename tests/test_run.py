# pylint: disable = redefined-outer-name
import os
import sys
from pathlib import Path
from tokenize import TokenInfo
from typing import List

import pytest

import pydocstringformatter
from pydocstringformatter.formatting import FORMATTERS, Formatter
from pydocstringformatter.run import _Run


def test_no_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that we display a help message when no arguments are provided."""
    sys.argv = ["pydocstringformatter"]
    pydocstringformatter.run_docstring_formatter()
    out, err = capsys.readouterr()
    assert out.startswith("usage: pydocstringformatter [-h]")

    # Test that we print help messages for individual formatters as well
    assert "--beginning-quotes" in out
    assert "Activate the beginning-quotes formatter" in out
    assert "--no-beginning-quotes" in out
    assert "Deactivate the beginning-quotes formatter" in out
    assert not err


def test_sys_agv_as_arguments(
    capsys: pytest.CaptureFixture[str], test_file: str
) -> None:
    """Test running with arguments in sys.argv"""
    sys.argv = ["pydocstringformatter", test_file]
    pydocstringformatter.run_docstring_formatter()

    with open(test_file, encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring"""'

    output = capsys.readouterr()
    assert output.out.endswith(
        '''
@@ -1,2 +1,3 @@
 """A multi-line
-docstring"""
+docstring
+"""'''
    )
    assert not output.err


def test_output_message_nothing_done(
    capsys: pytest.CaptureFixture[str], test_file: str
) -> None:
    """Test that we emit the correct message when nothing was done"""
    with open(test_file, "w", encoding="utf-8") as file:
        file.write('"""A multi-line\ndocstring\n"""')
    with open(test_file + "2", "w", encoding="utf-8") as file:
        file.write('"""A multi-line\ndocstring\n"""')

    pydocstringformatter.run_docstring_formatter(
        [str(Path(test_file).parent), "--write"]
    )

    output = capsys.readouterr()
    assert output.out == "Nothing to do! All docstrings are correct 🎉\n"
    assert not output.err


def test_output_message_one_file(
    capsys: pytest.CaptureFixture[str], test_file: str
) -> None:
    """Test that we emit the correct message when one out of two files was formatted"""
    try:
        expected_path = os.path.relpath(test_file)
    except ValueError:
        expected_path = test_file

    with open(test_file + "2", "w", encoding="utf-8") as file:
        file.write('"""A multi-line\ndocstring\n"""')

    pydocstringformatter.run_docstring_formatter(
        [str(Path(test_file).parent), "--write"]
    )

    output = capsys.readouterr()
    assert output.out == f"Formatted {expected_path} 📖\n"
    assert not output.err


def test_output_message_two_files(
    capsys: pytest.CaptureFixture[str], test_file: str
) -> None:
    """Test that we emit the correct message when two files were formatted"""
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


def test_optional_formatter(capsys: pytest.CaptureFixture[str]) -> None:
    """If a Formatter is optional we handle that in _load_default_formatter."""

    class OptionalFormatter(Formatter):
        """Non-optional docstring."""

        optional = True
        name = "optional-formatter"

        def treat_token(self, tokeninfo: TokenInfo) -> TokenInfo:
            """This does nothing"""
            return tokeninfo

    with pytest.raises(SystemExit):
        _Run(argv=["--help"], formatters=[OptionalFormatter()])
    out, err = capsys.readouterr()
    assert not err
    assert "--optional-formatter" in out
    assert "optional docstring." in out
    assert "--no-optional-formatter" in out


@pytest.mark.parametrize(
    "args,should_format",
    [
        [[f"--no-{f.name}" for f in FORMATTERS], False],
        [[f"--{f.name}" for f in FORMATTERS], True],
    ],
)
def test_optional_formatters(
    args: List[str],
    should_format: bool,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    """Test that (optional) formatters are activated or not depending on options."""
    bad_docstring = tmp_path / "bad_docstring.py"
    bad_docstring.write_text(f'"""{"a" * 120}\n{"b" * 120}"""')
    pydocstringformatter.run_docstring_formatter([str(bad_docstring)] + args)
    out, err = capsys.readouterr()
    assert not err
    if should_format:
        msg = "Nothing was modified, but all formatters are activated."
        assert "Nothing to do!" not in out
        expected = ["---", "@@", "+++"]
        assert all(e in out for e in expected), msg
    else:
        msg = "Something was modified, but all formatter are deactivated."
        assert "Nothing to do!" in out, msg
