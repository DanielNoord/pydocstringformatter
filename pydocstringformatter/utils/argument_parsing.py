import argparse
from typing import List


def _parse_arguments(
    parser: argparse.ArgumentParser, args: List[str]
) -> argparse.Namespace:
    """Parse all arguments on the provided argument parser"""
    return parser.parse_args(args)


def _register_arguments(version: str) -> argparse.ArgumentParser:
    """Create an argument parser and add all supported arguments"""
    parser = argparse.ArgumentParser(prog="pydocstringformatter")

    parser.add_argument("files", nargs="*", type=str)

    parser.add_argument(
        "-w",
        "--write",
        action="store_true",
        help="Write the changes to file instead of printing the files to stdout",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=version,
        help="Show version number and exit",
    )

    return parser
