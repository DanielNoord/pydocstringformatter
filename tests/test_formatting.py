import os
import pathlib
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


@pytest.mark.parametrize(
    "test_file",
    TESTS,
    ids=TEST_NAMES,
)
def test_formatting(
    test_file: str, capsys: pytest.CaptureFixture[str], tmp_path: pathlib.Path
) -> None:
    """Test that we correctly format all files in the format directory.

    We create and write to a temporary file so that the original test file
    isn't overwritten and the 'py.out' file can represent an actual
    python file instead of a diff.
    """
    # Setup
    temp_file_name = str(tmp_path / "test_file.py")
    with open(test_file + ".out", encoding="utf-8") as expected_output:
        expected_lines = expected_output.readlines()

    # Get original lines from test file and write to temporary file
    with open(test_file, encoding="utf-8") as original_file:
        original_lines = original_file.readlines()
    with open(temp_file_name, "w", encoding="utf-8") as temp_file:
        temp_file.writelines(original_lines)

    # Get any additional args as specified by an .args file
    additional_args: List[str] = []
    if os.path.exists(test_file.replace(".py", ".args")):
        with open(test_file.replace(".py", ".args"), encoding="utf-8") as args_file:
            additional_args = args_file.readlines()[0].split()

    pydocstringformatter.run_docstring_formatter(
        [temp_file_name, "--write"] + additional_args
    )

    output = capsys.readouterr()
    assert not output.err
    with open(temp_file_name, encoding="utf-8") as temp_file:
        assert temp_file.readlines() == expected_lines
