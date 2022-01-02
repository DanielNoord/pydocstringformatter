# pylint: disable = redefined-outer-name
import os
import sys

import pytest
from py._path.local import LocalPath

import pydocstringformatter


@pytest.fixture  # type: ignore[misc] # Decorator is untyped
def test_file(tmpdir: LocalPath) -> str:
    """A test file to be used by tests"""
    filename = tmpdir / "test.py"
    with open(filename, "w", encoding="utf-8") as file:
        file.write('"""A multi-line\ndocstring"""')
    return str(filename)


def test_no_arguments(capsys: pytest.CaptureFixture) -> None:
    """Test that we warn when no arguments are provided"""
    sys.argv = ["pydocstringformatter"]
    pydocstringformatter.run_docstring_formatter()
    output = capsys.readouterr()
    assert output.out.startswith("usage: pydocstringformatter [-h]")
    assert not output.err


def test_sys_agv_as_arguments(capsys: pytest.CaptureFixture, test_file: str) -> None:
    """Test running with arguments in sys.argv"""
    sys.argv = ["pydocstringformatter", test_file]
    pydocstringformatter.run_docstring_formatter()

    with open(test_file, encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring"""'

    output = capsys.readouterr()
    assert output.out == '"""A multi-line\ndocstring\n"""'
    assert not output.err


def test_no_write_argument(capsys: pytest.CaptureFixture, test_file: str) -> None:
    """Test that we print to stdout without the -w option"""
    pydocstringformatter.run_docstring_formatter([test_file])

    with open(test_file, encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring"""'

    output = capsys.readouterr()
    assert output.out == '"""A multi-line\ndocstring\n"""'
    assert not output.err


def test_write_argument(capsys: pytest.CaptureFixture, test_file: str) -> None:
    """Test the -w argument"""
    pydocstringformatter.run_docstring_formatter([test_file, "-w"])

    with open(test_file, encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring\n"""'

    output = capsys.readouterr()
    assert output.out == f"Formatted {os.path.relpath(test_file)} 📖\n"
    assert not output.err


def test_long_write_argument(capsys: pytest.CaptureFixture, test_file: str) -> None:
    """Test the --write argument"""
    pydocstringformatter.run_docstring_formatter([test_file, "--write"])

    with open(test_file, encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring\n"""'

    output = capsys.readouterr()
    assert output.out == f"Formatted {os.path.relpath(test_file)} 📖\n"
    assert not output.err


def test_version_argument(capsys: pytest.CaptureFixture) -> None:
    """Test the --version argument and its shorter variant"""
    with pytest.raises(SystemExit):
        pydocstringformatter.run_docstring_formatter(["--version"])
    output = capsys.readouterr()
    assert output.out == pydocstringformatter.__version__ + "\n"
    assert not output.err

    with pytest.raises(SystemExit):
        pydocstringformatter.run_docstring_formatter(["-v"])
    output = capsys.readouterr()
    assert output.out == pydocstringformatter.__version__ + "\n"
    assert not output.err
