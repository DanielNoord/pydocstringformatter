from __future__ import annotations

from pydocstringformatter._formatting import FORMATTERS


def test_formatter_names() -> None:
    """Test that each formatter name exists and is unique."""
    formatter_names: set[str] = set()
    for formatter in FORMATTERS:
        assert formatter.name, "Each formatter should have a name set."
        assert (
            formatter.name not in formatter_names
        ), "Each formatter should have an unique name."
        formatter_names.add(formatter.name)
