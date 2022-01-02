import os
from pathlib import Path
from typing import List

import pytest

import pydocstringformatter

HERE = Path(__file__)
TEST_DATA = HERE.parent / "data" / "format"

# Get all the test files
TESTS: List[str] = []
TEST_NAMES: List[str] = []
for dirname, _, files in os.walk(TEST_DATA):
    for file in files:
        if file.endswith(".py"):
            dirpath = Path(dirname)
            TESTS.append(str(dirpath / file))
            TEST_NAMES.append(f"{dirpath.stem}-{file}")


@pytest.mark.parametrize(  # type: ignore[misc] # Untyped decorator
    "test_file",
    TESTS,
    ids=TEST_NAMES,
)
def test_formatting(test_file: str, capsys: pytest.CaptureFixture) -> None:
    """Test that we correctly format all files in the format directory"""
    pydocstringformatter.run_docstring_formatter([test_file])
    output = capsys.readouterr()
    assert not output.err
    with open(test_file + ".out", encoding="utf-8") as expected_output:
        assert output.out == "".join(expected_output.readlines())
