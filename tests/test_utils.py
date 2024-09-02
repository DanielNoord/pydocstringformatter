from __future__ import annotations

import sys
import tokenize
from pathlib import Path

import pytest

import pydocstringformatter
from pydocstringformatter._testutils import MakeAFormatter, MakeBFormatter
from pydocstringformatter._utils import (
    compare_formatters,
    find_python_files,
    is_docstring,
)

HERE = Path(__file__)
UTILS_DATA = HERE.parent / "data" / "utils"


class TestPythonFileFinder:
    """Test the python file finder."""

    @staticmethod
    def test_underscores_files() -> None:
        """Test that we can find files with leading underscores."""
        pathnames = find_python_files([str(UTILS_DATA / "find_underscore_files")], [])
        expected_paths = [
            UTILS_DATA / "find_underscore_files" / "file_one.py",
            UTILS_DATA / "find_underscore_files" / "_file_two.py",
            UTILS_DATA / "find_underscore_files" / "__file_three.py",
            UTILS_DATA / "find_underscore_files" / "____file_five.py",
        ]
        assert sorted(expected_paths) == pathnames

    @staticmethod
    def test_recursive_files() -> None:
        """Test that we can find files recursively."""
        pathnames = find_python_files(
            [str(UTILS_DATA / "find_recursive_files")], [], recursive=True
        )
        expected_paths = [
            UTILS_DATA / "find_recursive_files" / "file_one.py",
            UTILS_DATA
            / "find_recursive_files"
            / "inner_directory"
            / "inner_file_one.py",
            UTILS_DATA
            / "find_recursive_files"
            / "inner_directory"
            / "inner_inner_directory"
            / "inner_inner_file_one.py",
        ]
        assert sorted(expected_paths) == pathnames

    @staticmethod
    def test_recursive_files_standard() -> None:
        """Test that we can find files recursively even if argument is not supplied."""
        pathnames = find_python_files([str(UTILS_DATA / "find_recursive_files")], [])
        expected_paths = [
            UTILS_DATA / "find_recursive_files" / "file_one.py",
            UTILS_DATA
            / "find_recursive_files"
            / "inner_directory"
            / "inner_file_one.py",
            UTILS_DATA
            / "find_recursive_files"
            / "inner_directory"
            / "inner_inner_directory"
            / "inner_inner_file_one.py",
        ]
        assert sorted(expected_paths) == pathnames

    @staticmethod
    def test_ignore_recursive_files() -> None:
        """Test that we ignore inner directories if recusrive is False."""
        pathnames = find_python_files(
            [str(UTILS_DATA / "find_recursive_files")], [], recursive=False
        )
        expected_paths = [UTILS_DATA / "find_recursive_files" / "file_one.py"]
        assert sorted(expected_paths) == pathnames

    @staticmethod
    def test_ignore_non_python_file() -> None:
        """Test that we ignore a non Python file."""
        pathnames = find_python_files(
            [str(UTILS_DATA / "find_nothing" / "README.md")], []
        )
        assert not pathnames


class TestDocstringFinder:
    """Test the docstring finder."""

    docstring_data = UTILS_DATA / "find_docstrings"

    def test_function_docstrings(self) -> None:
        """Test that we can find docstrings for function definitions."""
        docstrings: list[tuple[tuple[int, int], tuple[int, int]]] = []
        with open(
            self.docstring_data / "function_docstrings.py", encoding="utf-8"
        ) as file:
            tokens = list(tokenize.generate_tokens(file.readline))
            for index, tokeninfo in enumerate(tokens):
                if is_docstring(tokeninfo, tokens[index - 1]):
                    docstrings.append((tokeninfo.start, tokeninfo.end))

        assert docstrings == [
            ((2, 4), (2, 21)),
            ((5, 8), (5, 25)),
            ((9, 4), (10, 16)),
            ((13, 8), (14, 20)),
            ((18, 4), (20, 7)),
            ((23, 8), (25, 11)),
            ((29, 4), (29, 21)),
            ((32, 8), (32, 25)),
            ((36, 4), (37, 16)),
            ((40, 8), (41, 20)),
            ((45, 4), (47, 7)),
            ((50, 8), (52, 11)),
        ]

    def test_dictionary_key_value_line(self) -> None:
        """Test that string key-value pairs are not considered a docstring."""
        with open(self.docstring_data / "dictionary.py", encoding="utf-8") as file:
            tokens = list(tokenize.generate_tokens(file.readline))
            for index, tokeninfo in enumerate(tokens):
                assert not is_docstring(tokeninfo, tokens[index - 1])

    def test_module_docstrings(self) -> None:
        """Test that we find the correct module docstring."""
        docstrings: list[tuple[tuple[int, int], tuple[int, int]]] = []
        with open(
            self.docstring_data / "module_docstrings.py", encoding="utf-8"
        ) as file:
            tokens = list(tokenize.generate_tokens(file.readline))
            for index, tokeninfo in enumerate(tokens):
                if is_docstring(tokeninfo, tokens[index - 1]):
                    docstrings.append((tokeninfo.start, tokeninfo.end))

        assert docstrings == [((3, 0), (4, 3))]


def test_encoding_of_console_messages(
    capsys: pytest.CaptureFixture[str], test_file: str
) -> None:
    """Test that we can print emoji's to non utf-8 consoles.

    Regression test for:
    https://github.com/DanielNoord/pydocstringformatter/issues/13
    """
    sys.stdout.reconfigure(encoding="cp1252")  # type: ignore[union-attr]
    with open(test_file, "w", encoding="utf-8") as file:
        file.write('"""A multi-line.\n\ndocstring.\n"""')

    pydocstringformatter.run_docstring_formatter([test_file, "--write"])

    output = capsys.readouterr()
    assert output.out == "Nothing to do! All docstrings in 1 file are correct 🎉\n"
    assert not output.err


def test_formatter_comparer() -> None:
    """Test the compare_formatters utility function."""
    tokeninfo = tokenize.TokenInfo(
        1, '"""AAA AA AAA"""', (1, 0), (1, 0), '"""AAA AA AAA"""'
    )

    diff = compare_formatters(tokeninfo, MakeAFormatter(), MakeBFormatter(), "test")

    expected_sections = [
        "--- make-a-formatter vs make-b-formatter test\n",
        '-"""AAA AA AAA"""\n',
        '+"""BBB BB BBB"""\n',
    ]

    for section in expected_sections:
        assert section in diff

    diff = compare_formatters(tokeninfo, MakeAFormatter(), MakeBFormatter())

    expected_sections = [
        "--- make-a-formatter vs make-b-formatter\n",
        '-"""AAA AA AAA"""\n',
        '+"""BBB BB BBB"""\n',
    ]

    for section in expected_sections:
        assert section in diff
