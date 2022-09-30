from pathlib import Path
from unittest.mock import patch

import pytest

from pydocstringformatter import _utils, run_docstring_formatter
from pydocstringformatter.run import _Run

HERE = Path(__file__)
DATA = HERE.parent / "data"


def test_exception_on_incorrect_python() -> None:
    """Test that we raise the correct exception on unparsable python files."""
    with pytest.raises(_utils.ParsingError):
        run_docstring_formatter([str(DATA / "incorrect_python_file.py")])


@patch(
    "pydocstringformatter._formatting.FinalPeriodFormatter.treat_token",
    RuntimeError,
)
def test_exception_on_unexpected_crash(
    test_file: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test that we print a user-friendly crash report on unexpected error."""
    run_docstring_formatter(["pydocstringformatter", test_file])
    _Run(["test_package"])
    out, err = capsys.readouterr()
    assert "Nothing to do!" in out
    assert "RuntimeError" in err
    assert "Please open an issue at https:" in err
