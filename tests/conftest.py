import pytest
from py._path.local import LocalPath


@pytest.fixture
def test_file(tmpdir: LocalPath) -> str:
    """A test file to be used by tests"""
    filename = tmpdir / "test.py"
    with open(filename, "w", encoding="utf-8") as file:
        file.write('"""A multi-line\ndocstring"""')
    return str(filename)
