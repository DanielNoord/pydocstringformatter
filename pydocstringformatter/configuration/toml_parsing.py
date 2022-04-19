from __future__ import annotations

import argparse
import os
from typing import Any, Final

import tomli

from pydocstringformatter.utils.exceptions import TomlParsingError, UnrecognizedOption

OPTIONS_TYPES: Final = {"write": "store_true", "exclude": "store"}


def _get_toml_file() -> dict[str, Any] | None:
    """See if there is a pyproject.toml and extract the correct section if it exists."""
    if os.path.isfile("pyproject.toml"):
        with open("pyproject.toml", "rb") as file:
            try:
                toml_dict = tomli.load(file)
            except tomli.TOMLDecodeError as exc:
                raise TomlParsingError from exc
            if tool_section := toml_dict.get("tool", None):
                if pydocformat_sect := tool_section.get("pydocstringformatter", None):
                    assert isinstance(pydocformat_sect, dict)
                    return pydocformat_sect
    return None


def _parse_toml_option(opt: str, value: Any) -> list[str]:
    """Parse an options value in the correct argument type for argparse."""
    try:
        action = OPTIONS_TYPES[opt]
    except KeyError as exc:
        raise UnrecognizedOption(f"Don't recognize option {opt}") from exc

    if action == "store_true":
        if value is True:
            return [f"--{opt}"]
        return []
    if action == "store":
        return [f"--{opt}", value]
    return []  # pragma: no cover


def _parse_toml_file(
    parser: argparse.ArgumentParser, namespace: argparse.Namespace
) -> None:
    """Get and parse the relevant section form a pyproject.toml file."""
    if toml_sect := _get_toml_file():
        arguments: list[str] = []

        for key, value in toml_sect.items():
            arguments += _parse_toml_option(key, value)

        parser.parse_args(arguments, namespace)
