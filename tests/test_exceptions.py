from pathlib import Path

import pytest

from pydocstringformatter import run_docstring_formatter, utils

HERE = Path(__file__)
DATA = HERE.parent / "data"


def test_exception_on_incorrect_python() -> None:
    """Test that we raise the correct exception on unparsable python files"""
    with pytest.raises(utils.ParsingError):
        run_docstring_formatter([str(DATA / "incorrect_python_file.py")])
