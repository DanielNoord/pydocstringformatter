import token
import tokenize
from pathlib import Path

from pydocstringformatter.utils import _find_python_files, _is_docstring

HERE = Path(__file__)
UTILS_DATA = HERE.parent / "data" / "utils"


class TestPythonFileFinder:
    """Test the python file finder"""

    @staticmethod
    def test_underscores_files() -> None:
        """Test that we can find files with leading underscores"""
        pathnames = _find_python_files([str(UTILS_DATA / "find_underscore_files")])
        expected_paths = [
            UTILS_DATA / "find_underscore_files" / "file_one.py",
            UTILS_DATA / "find_underscore_files" / "_file_two.py",
            UTILS_DATA / "find_underscore_files" / "__file_three.py",
            UTILS_DATA / "find_underscore_files" / "____file_five.py",
        ]
        assert sorted(expected_paths) == pathnames

    @staticmethod
    def test_recursive_files() -> None:
        """Test that we can find files recursively"""
        pathnames = _find_python_files(
            [str(UTILS_DATA / "find_recursive_files")], recursive=True
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
        """Test that we can find files recursively even if argument is not supplied"""
        pathnames = _find_python_files([str(UTILS_DATA / "find_recursive_files")])
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
        """Test that we ignore inner directories if recusrive is False"""
        pathnames = _find_python_files(
            [str(UTILS_DATA / "find_recursive_files")], recursive=False
        )
        expected_paths = [UTILS_DATA / "find_recursive_files" / "file_one.py"]
        assert sorted(expected_paths) == pathnames


class TestDocstringFinder:
    """Test the docstring finder"""

    docstring_data = UTILS_DATA / "find_docstrings"

    def test_function_docstrings(self) -> None:
        """Test that we can find docstrings for function definitions"""
        docstrings: list[tuple[tuple[int, int], tuple[int, int]]] = []
        with open(
            self.docstring_data / "function_docstrings.py", encoding="utf-8"
        ) as file:
            tokens = list(tokenize.generate_tokens(file.readline))
            for index, tokeninfo in enumerate(tokens):
                if _is_docstring(tokeninfo, tokens[index - 1]):
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
        """Test that we do not classify a line of string key and value pairs as docstring"""
        docstrings: list[tuple[tuple[int, int], tuple[int, int]]] = []
        with open(self.docstring_data / "dictionary.py", encoding="utf-8") as file:
            tokens = list(tokenize.generate_tokens(file.readline))
            for index, tokeninfo in enumerate(tokens):
                if _is_docstring(tokeninfo, tokens[index - 1]):
                    docstrings.append((tokeninfo.start, tokeninfo.end))

        assert docstrings == []
