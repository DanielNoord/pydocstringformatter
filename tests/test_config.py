# pylint: disable=trailing-whitespace

import os
from pathlib import Path

import pytest

import pydocstringformatter
from pydocstringformatter._utils import exceptions
from pydocstringformatter.run import _Run

HERE = Path(__file__)
CONFIG_DATA = HERE.parent / "data" / "config"


def test_no_toml(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test a directory without a pyproject.toml."""
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
    """Test a correct toml with write = True."""
    monkeypatch.chdir(CONFIG_DATA / "valid_toml")
    pydocstringformatter.run_docstring_formatter(["test_package"])
    output = capsys.readouterr()
    assert output.out == "Nothing to do! All docstrings in 1 file are correct 🎉\n"
    assert not output.err


def test_valid_toml_two(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test a correct toml with write = False."""
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
    """Test an invalid toml file."""
    monkeypatch.chdir(CONFIG_DATA / "invalid_toml")
    with pytest.raises(exceptions.TomlParsingError):
        pydocstringformatter.run_docstring_formatter(["test_package"])


def test_non_existing_options(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test an toml file with unrecognized options."""
    monkeypatch.chdir(CONFIG_DATA / "non_existing_options")
    with pytest.raises(exceptions.UnrecognizedOption):
        pydocstringformatter.run_docstring_formatter(["test_package"])


def test_no_write_argument(capsys: pytest.CaptureFixture[str], test_file: str) -> None:
    """Test that we print to stdout without the -w option."""
    pydocstringformatter.run_docstring_formatter([test_file])

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


def test_write_argument(capsys: pytest.CaptureFixture[str], test_file: str) -> None:
    """Test the -w argument."""
    try:
        expected_path = os.path.relpath(test_file)
    except ValueError:
        expected_path = test_file

    pydocstringformatter.run_docstring_formatter([test_file, "-w"])

    with open(test_file, encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line.\n\ndocstring.\n"""'

    output = capsys.readouterr()
    assert output.out == f"Formatted {expected_path} 📖\n"
    assert not output.err


def test_long_write_argument(
    capsys: pytest.CaptureFixture[str], test_file: str
) -> None:
    """Test the --write argument."""
    try:
        expected_path = os.path.relpath(test_file)
    except ValueError:
        expected_path = test_file

    pydocstringformatter.run_docstring_formatter([test_file, "--write"])

    with open(test_file, encoding="utf-8") as file:
        assert "".join(file.readlines()) == '"""A multi-line.\n\ndocstring.\n"""'

    output = capsys.readouterr()
    assert output.out == f"Formatted {expected_path} 📖\n"
    assert not output.err


def test_version_argument(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the --version argument and its shorter variant."""
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
    """Tests for the --exclude option."""

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
        assert output.out == "Nothing to do! All docstrings in 0 files are correct 🎉\n"
        assert not output.err

    @staticmethod
    def test_exclude_match_inner_directory(
        capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test when the inner directory matches the pattern."""
        monkeypatch.chdir(CONFIG_DATA / "exclude_match_inner")
        pydocstringformatter.run_docstring_formatter(["test_package"])
        output = capsys.readouterr()
        assert output.out == "Nothing to do! All docstrings in 0 files are correct 🎉\n"
        assert not output.err

    @staticmethod
    def test_exclude_csv_string(
        capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test when there is a match with a string in a csv string."""
        monkeypatch.chdir(CONFIG_DATA / "exclude_match_csv")
        pydocstringformatter.run_docstring_formatter(["test_package"])
        output = capsys.readouterr()
        assert output.out == "Nothing to do! All docstrings in 0 files are correct 🎉\n"
        assert not output.err

    @staticmethod
    def test_exclude_csv_list(
        capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test when there is a match with a string in a list of strings."""
        monkeypatch.chdir(CONFIG_DATA / "exclude_match_csv_list")
        pydocstringformatter.run_docstring_formatter(["test_package"])
        output = capsys.readouterr()
        assert output.out == "Nothing to do! All docstrings in 0 files are correct 🎉\n"
        assert not output.err

    @staticmethod
    def test_quiet_argument(capsys: pytest.CaptureFixture[str], test_file: str) -> None:
        """Test the --quiet argument."""
        pydocstringformatter.run_docstring_formatter([test_file, "-w", "--quiet"])

        with open(test_file, encoding="utf-8") as file:
            assert "".join(file.readlines()) == '"""A multi-line.\n\ndocstring.\n"""'

        output = capsys.readouterr()
        assert not output.out
        assert not output.err


class TestStyleOption:
    """Tests for the --style option."""

    def test_style_default(self, test_file: str) -> None:
        """Test that the default value of --style is pep257."""
        run = _Run([test_file])
        assert run.config.style == ["pep257"]

    def test_style_pep257(self, test_file: str) -> None:
        """Test that we don't duplicate the default value if we pass it again."""
        run = _Run([test_file, "--style", "pep257"])
        assert run.config.style == ["pep257"]

    def test_style_numpydoc_only(self, test_file: str) -> None:
        """Test that we can specify only a non-default style."""
        run = _Run([test_file, "--style", "numpydoc"])
        assert ["numpydoc"] == run.config.style

    def test_style_invalid_choice(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that we correctly reject invalid styles."""
        with pytest.raises(SystemExit) as excinfo:
            _Run(["--style", "invalid"])
        assert excinfo.value.code == 2

        output = capsys.readouterr()
        assert not output.out
        assert "--style: invalid choice: 'invalid'" in output.err

    def test_style_in_toml(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that the style argument works in the toml file."""
        monkeypatch.chdir(CONFIG_DATA / "valid_toml_numpydoc")
        run = _Run(["test_package"])
        assert ["numpydoc"] == run.config.style

        monkeypatch.chdir(CONFIG_DATA / "valid_toml_pep257")
        run = _Run(["test_package"])
        assert ["pep257"] == run.config.style

        monkeypatch.chdir(CONFIG_DATA / "valid_toml_numpydoc_pep257")
        run = _Run(["test_package"])
        assert run.config.style == ["numpydoc", "pep257"]

    def test_boolopt_in_toml(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that arguments of type BooleanOptionalAction work in toml files."""
        monkeypatch.chdir(CONFIG_DATA / "valid_toml_boolopt")
        run = _Run(["test_package"])
        assert not run.config.summary_quotes_same_line

        # dashes in the name dont allow the dot notation to get this value
        assert not run.config.__dict__["numpydoc-section-hyphen-length"]
        assert run.config.__dict__["strip-whitespaces"]

    def test_non_valid_boolopt_in_toml(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that '--no' versions of BooleanOptionalAction in toml do not work."""
        monkeypatch.chdir(CONFIG_DATA / "non_valid_toml_boolopt")
        with pytest.raises(exceptions.TomlParsingError) as err:
            _Run(["test_package"])

        error_msg = (
            "TOML file contains an unsupported option "
            "'no-numpydoc-section-hyphen-length: true', try using "
            "'numpydoc-section-hyphen-length: false' instead"
        )

        assert error_msg in str(err.value)

    def test_non_bool_boolopt_in_toml(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that non-bool values of BooleanOptionalAction in toml do not work."""
        monkeypatch.chdir(CONFIG_DATA / "non_valid_toml_boolopt_two")
        with pytest.raises(ValueError) as err:
            _Run(["test_package"])

        error_msg = (
            "{'true'} <class 'str'> is not a supported argument"
            " for 'numpydoc-section-hyphen-length',"
            " please use either {true} or {false}."
        )

        assert error_msg in str(err.value)

    def test_valid_toml_without_section(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that we leave a projecttoml without a section for this tool alone."""
        monkeypatch.chdir(CONFIG_DATA / "valid_toml_without_section")
        _Run(["test_package"])
