from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import pytest

from pydocstringformatter import _formatting
from pydocstringformatter import _testutils as test_utils
from pydocstringformatter._formatting import Formatter
from pydocstringformatter._utils import UnstableResultError
from pydocstringformatter.run import _Run


@contextmanager
def patched_run(formatters: list[Formatter]) -> Generator[type[_Run]]:
    """Patches formatters so Run only uses the provided formatters."""
    old_formatters = _formatting.FORMATTERS
    _formatting.FORMATTERS = formatters
    yield _Run
    _formatting.FORMATTERS = old_formatters


@pytest.mark.parametrize(
    "formatters,expected_errors",
    [
        (
            [test_utils.MakeAFormatter(), test_utils.MakeBFormatter()],
            ["Conflicting formatters"],
        ),
        (
            [test_utils.MakeBFormatter(), test_utils.AddBFormatter()],
            ["not able to make stable changes"],
        ),
        (
            [
                test_utils.MakeBFormatter(),
                test_utils.AddBFormatter(),
                test_utils.MakeAFormatter(),
            ],
            ["Conflicting formatters:", "Diff too intricate to compute"],
        ),
    ],
)
def test_conflicting_formatters(
    formatters: list[Formatter],
    expected_errors: list[str],
    tmp_path: Path,
) -> None:
    """Tests that conflicting formatters raise an error."""
    tmp_file = tmp_path / "test.py"
    with open(tmp_file, "w", encoding="utf-8") as f:
        content = [
            '"""AAA AA AAA"""',
        ]
        f.writelines(content)

    with patched_run(formatters) as run:
        with pytest.raises(UnstableResultError) as err:
            run([str(tmp_file)])

    for expect_err in expected_errors:
        assert expect_err in str(err.value), str(err.value)
