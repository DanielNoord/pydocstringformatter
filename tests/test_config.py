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
    assert output.out == '"""A docstring"""\n'
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
    assert output.out == '"""A docstring"""\n'
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
