import sys
from pathlib import Path

import pydocstringformatter
import pytest


@pytest.fixture
def test_file(tmpdir: Path) -> str:
    """A test file to be used by tests"""
    filename = tmpdir.join("test.py")
    with open(filename, "w", encoding="utf-8") as file:
        file.write('"""A multi-line\ndocstring"""')
    return str(filename)


def test_no_arguments(capsys: pytest.CaptureFixture) -> None:
    """Test that we warn when no arguments are provided"""
    pydocstringformatter.run_docstring_formatter()
    output = capsys.readouterr()
    assert output.out.startswith("usage: pydocstringformatter [-h]")
    assert not output.err


def test_sys_agv_as_arguments(capsys: pytest.CaptureFixture, test_file: str) -> None:
    """Test running with arguments in sys.argv"""
    sys.argv = ["pydocstringformatter", test_file]
    pydocstringformatter.run_docstring_formatter()

    with open(test_file, "r", encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring"""'

    output = capsys.readouterr()
    assert output.out == '"""A multi-line\ndocstring\n"""'
    assert not output.err


def test_no_write_argument(capsys: pytest.CaptureFixture, test_file: str) -> None:
    """Test that we print to stdout without the -w option"""
    pydocstringformatter.run_docstring_formatter([test_file])

    with open(test_file, "r", encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring"""'

    output = capsys.readouterr()
    assert output.out == '"""A multi-line\ndocstring\n"""'
    assert not output.err


def test_write_argument(capsys: pytest.CaptureFixture, test_file: str) -> None:
    """Test the -w argument"""
    pydocstringformatter.run_docstring_formatter([test_file, "-w"])

    with open(test_file, "r", encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring\n"""'

    output = capsys.readouterr()
    assert not output.out
    assert not output.err


def test_long_write_argument(capsys: pytest.CaptureFixture, test_file: str) -> None:
    """Test the --write argument"""
    pydocstringformatter.run_docstring_formatter([test_file, "--write"])

    with open(test_file, "r", encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring\n"""'

    output = capsys.readouterr()
    assert not output.out
    assert not output.err
