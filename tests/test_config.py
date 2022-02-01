import os
from pathlib import Path

import pytest

import pydocstringformatter
from pydocstringformatter.utils import exceptions

HERE = Path(__file__)
CONFIG_DATA = HERE.parent / "data" / "config"


def test_no_toml(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test a directory without a pyproject.toml"""
    monkeypatch.chdir(CONFIG_DATA / "no_toml")
    pydocstringformatter.run_docstring_formatter(["test_package"])
    output = capsys.readouterr()
    assert output.out.endswith(
        '''
@@ -1,3 +1,2 @@
-"""
-A docstring"""
+"""A docstring."""
 '''
    )
    assert not output.err


def test_valid_toml(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test a correct toml with write = True"""
    monkeypatch.chdir(CONFIG_DATA / "valid_toml")
    pydocstringformatter.run_docstring_formatter(["test_package"])
    output = capsys.readouterr()
    assert output.out == "Nothing to do! All docstrings are correct 🎉\n"
    assert not output.err


def test_valid_toml_two(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test a correct toml with write = False"""
    monkeypatch.chdir(CONFIG_DATA / "valid_toml_two")
    pydocstringformatter.run_docstring_formatter(["test_package"])
    output = capsys.readouterr()
    assert output.out.endswith(
        '''
@@ -1,3 +1,2 @@
-"""
-A docstring"""
+"""A docstring."""
 '''
    )
    assert not output.err


def test_invalid_toml(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test an invalid toml file"""
    monkeypatch.chdir(CONFIG_DATA / "invalid_toml")
    with pytest.raises(exceptions.TomlParsingError):
        pydocstringformatter.run_docstring_formatter(["test_package"])


def test_non_existing_options(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test an toml file with unrecognized options"""
    monkeypatch.chdir(CONFIG_DATA / "non_existing_options")
    with pytest.raises(exceptions.UnrecognizedOption):
        pydocstringformatter.run_docstring_formatter(["test_package"])


def test_no_write_argument(capsys: pytest.CaptureFixture[str], test_file: str) -> None:
    """Test that we print to stdout without the -w option"""
    pydocstringformatter.run_docstring_formatter([test_file])

    with open(test_file, encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring"""'

    output = capsys.readouterr()
    assert output.out.endswith(
        '''
@@ -1,2 +1,3 @@
 """A multi-line
-docstring"""
+docstring\n+"""'''
    )
    assert not output.err


def test_write_argument(capsys: pytest.CaptureFixture[str], test_file: str) -> None:
    """Test the -w argument"""
    try:
        expected_path = os.path.relpath(test_file)
    except ValueError:
        expected_path = test_file

    pydocstringformatter.run_docstring_formatter([test_file, "-w"])

    with open(test_file, encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring\n"""'

    output = capsys.readouterr()
    assert output.out == f"Formatted {expected_path} 📖\n"
    assert not output.err


def test_long_write_argument(
    capsys: pytest.CaptureFixture[str], test_file: str
) -> None:
    """Test the --write argument"""
    try:
        expected_path = os.path.relpath(test_file)
    except ValueError:
        expected_path = test_file

    pydocstringformatter.run_docstring_formatter([test_file, "--write"])

    with open(test_file, encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line\ndocstring\n"""'

    output = capsys.readouterr()
    assert output.out == f"Formatted {expected_path} 📖\n"
    assert not output.err


def test_version_argument(capsys: pytest.CaptureFixture[str]) -> None:
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


class TestExcludeOption:
    """Tests for the --exclude option"""

    @staticmethod
    def test_exclude_non_match(
        capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test when there is no match with the pattern."""
        monkeypatch.chdir(CONFIG_DATA / "exclude_non_match")
        pydocstringformatter.run_docstring_formatter(["test_package"])
        output = capsys.readouterr()
        assert output.out.endswith(
            '''
@@ -1,3 +1,2 @@
-"""
-A docstring"""
+"""A docstring."""
 '''
        )
        assert not output.err

    @staticmethod
    def test_exclude_match(
        capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test when the directory matches the pattern."""
        monkeypatch.chdir(CONFIG_DATA / "exclude_match")
        pydocstringformatter.run_docstring_formatter(["test_package"])
        output = capsys.readouterr()
        assert output.out == "Nothing to do! All docstrings are correct 🎉\n"
        assert not output.err

    @staticmethod
    def test_exclude_match_inner_directory(
        capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test when the inner directory matches the pattern."""
        monkeypatch.chdir(CONFIG_DATA / "exclude_match_inner")
        pydocstringformatter.run_docstring_formatter(["test_package"])
        output = capsys.readouterr()
        assert output.out == "Nothing to do! All docstrings are correct 🎉\n"
        assert not output.err

    @staticmethod
    def test_exclude_csv_string(
        capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test when there is a match with a string in a csv string."""
        monkeypatch.chdir(CONFIG_DATA / "exclude_match_csv")
        pydocstringformatter.run_docstring_formatter(["test_package"])
        output = capsys.readouterr()
        assert output.out == "Nothing to do! All docstrings are correct 🎉\n"
        assert not output.err

    @staticmethod
    def test_exclude_csv_list(
        capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test when there is a match with a string in a list of strings."""
        monkeypatch.chdir(CONFIG_DATA / "exclude_match_csv_list")
        pydocstringformatter.run_docstring_formatter(["test_package"])
        output = capsys.readouterr()
        assert output.out == "Nothing to do! All docstrings are correct 🎉\n"
        assert not output.err
