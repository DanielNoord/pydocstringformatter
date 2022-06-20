from pathlib import Path

PRIMER_DIRECTORY_PATH = (
    Path(__file__).parent.parent.parent.parent / ".pydocstringformatter_primer_tests"
)
"""Directory to store anything primer related in."""

DIFF_OUTPUT = PRIMER_DIRECTORY_PATH / "fulldiff.txt"
"""Diff output file location."""
