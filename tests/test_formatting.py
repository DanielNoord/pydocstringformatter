from __future__ import annotations

import os
import pathlib
from pathlib import Path

import pytest

import pydocstringformatter
from pydocstringformatter._testutils import UPDATE_OUTPUT_OPTION

HERE = Path(__file__)
TEST_DATA = HERE.parent / "data" / "format"

# Get all the test files
TESTS: list[str] = []
TEST_NAMES: list[str] = []
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
    test_file: str,
    capsys: pytest.CaptureFixture[str],
    tmp_path: pathlib.Path,
    request: pytest.FixtureRequest,
) -> None:
    """Test that we correctly format all files in the format directory.

    We create and write to a temporary file so that the original test file
    isn't overwritten and the 'py.out' file can represent an actual
    python file instead of a diff.

    Everything is tested in bytes as we want to preserve the type of the
    line endings of the original file.
    """
    # Setup
    temp_file_name = str(tmp_path / "test_file.py")

    # Check if there is a specific output for the standard newline of this OS.
    # For example, this allows testing that in files without any initial newlines
    # we use the standard newline whenever we need one.
    test_name = f"{test_file}-{os.linesep.encode().hex()}.out"
    if not os.path.isfile(test_name):
        # This is the regular output file.
        test_name = test_file + ".out"

    with open(test_name, "rb") as f:
        expected_output = f.read()

    # Get original lines from test file and write to temporary file
    with open(test_file, "rb") as f:
        original_bytes = f.read()
    with open(temp_file_name, "wb") as f:
        f.write(original_bytes)

    # Get any additional args as specified by an .args file
    additional_args: list[str] = []
    if os.path.exists(test_file.replace(".py", ".args")):
        with open(test_file.replace(".py", ".args"), encoding="utf-8") as f:
            additional_args = [i.rstrip("\n") for i in f.readlines()]

    # Get message on stderr
    if os.path.exists(test_file.replace(".py", ".err")):
        with open(test_file.replace(".py", ".err"), encoding="utf-8") as f:
            error_message = f.read()
    else:
        error_message = ""

    pydocstringformatter.run_docstring_formatter(
        [temp_file_name, "--write"] + additional_args
    )

    error_output = capsys.readouterr()
    assert error_output.err == error_message.format(
        testfile=os.path.abspath(temp_file_name)
    )
    with open(temp_file_name, "rb") as f:
        output = f.read()
        try:
            assert output.decode("utf-8") == expected_output.decode("utf-8")
        except AssertionError as e:  # pragma: no cover
            if request.config.getoption(UPDATE_OUTPUT_OPTION):
                with open(test_name, "wb") as fw:
                    fw.write(output)
                pytest.fail(
                    "Updated expected output. Please check the changes and commit them."
                )

            raise AssertionError(
                f"Output of '{Path(test_file).stem}' does not match expected output. "
                f"Run with '{UPDATE_OUTPUT_OPTION}' to update the expected output."
            ) from e
