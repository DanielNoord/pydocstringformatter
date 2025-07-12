from pathlib import Path

import pytest

from pydocstringformatter._testutils import UPDATE_OUTPUT_OPTION


@pytest.fixture
def test_file(tmp_path: Path) -> str:
    """A test file to be used by tests."""
    filename = tmp_path / "test.py"
    with open(filename, "w", encoding="utf-8") as file:
        file.write('"""A multi-line\ndocstring."""')
    return str(filename)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add command line options to pytest."""
    parser.addoption(
        UPDATE_OUTPUT_OPTION,
        action="store_true",
        help="Update the expected output for tests. This will overwrite the output "
        "files to be as the tests are currently producing them.",
        default=False,
    )
