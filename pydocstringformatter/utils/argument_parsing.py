import argparse
import os
from typing import Any, Dict, List, Optional

import tomli

from pydocstringformatter.utils.exceptions import TomlParsingError, UnrecognizedOption

OPTIONS_TYPES = {"write": "store_true"}


def _parse_command_line_arguments(
    parser: argparse.ArgumentParser, args: List[str], namespace: argparse.Namespace
) -> None:
    """Parse all arguments on the provided argument parser."""
    parser.parse_known_args(args, namespace)


def _register_arguments(version: str) -> argparse.ArgumentParser:
    """Create an argument parser and add all supported arguments."""
    parser = argparse.ArgumentParser(prog="pydocstringformatter")

    parser.add_argument("files", nargs="*", type=str)

    parser.add_argument(
        "-w",
        "--write",
        action="store_true",
        help="Write the changes to file instead of printing the diffs to stdout",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=version,
        help="Show version number and exit",
    )

    return parser


def _get_toml_file() -> Optional[Dict[str, Any]]:
    """See if there is a pyproject.toml and extract the correct section if it exists."""
    if os.path.isfile("pyproject.toml"):
        with open("pyproject.toml", "rb") as file:
            try:
                toml_dict = tomli.load(file)
            except tomli.TOMLDecodeError as exc:
                raise TomlParsingError from exc
            if tool_section := toml_dict.get("tool", None):
                if pydocformat_sect := tool_section.get("pydocstringformatter", None):
                    assert isinstance(pydocformat_sect, Dict)
                    return pydocformat_sect
    return None


def _parse_toml_option(opt: str, value: Any) -> List[str]:
    """Parse an options value in the correct argument type for argparse."""
    try:
        action = OPTIONS_TYPES[opt]
    except KeyError as exc:
        raise UnrecognizedOption(f"Don't recognize option {opt}") from exc

    if action == "store_true":
        if value is True:
            return [f"--{opt}"]
        return []
    return []  # pragma: no cover


def _parse_toml_file(
    parser: argparse.ArgumentParser, namespace: argparse.Namespace
) -> None:
    """Get and parse the relevant section form a pyproject.toml file."""
    if toml_sect := _get_toml_file():
        arguments: List[str] = []

        for key, value in toml_sect.items():
            arguments += _parse_toml_option(key, value)

        parser.parse_args(arguments, namespace)
