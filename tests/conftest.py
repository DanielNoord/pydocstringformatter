import pytest
from pathlib import Path


@pytest.fixture
def test_file(tmp_path: Path) -> str:
    """A test file to be used by tests."""
    filename = tmp_path / "test.py"
    with open(filename, "w", encoding="utf-8") as file:
        file.write('"""A multi-line\ndocstring."""')
    return str(filename)
