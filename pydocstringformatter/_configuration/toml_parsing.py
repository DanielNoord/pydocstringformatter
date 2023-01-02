from __future__ import annotations

import argparse
import os
import sys
from typing import Any

from pydocstringformatter._configuration.boolean_option_action import (
    BooleanOptionalAction,
)
from pydocstringformatter._utils.exceptions import TomlParsingError, UnrecognizedOption

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib


def get_toml_file() -> dict[str, Any] | None:
    """See if there is a pyproject.toml and extract the correct section if it exists."""
    if os.path.isfile("pyproject.toml"):
        with open("pyproject.toml", "rb") as file:
            try:
                toml_dict = tomllib.load(file)
            except tomllib.TOMLDecodeError as exc:
                raise TomlParsingError from exc
            if tool_section := toml_dict.get("tool", None):
                if pydocformat_sect := tool_section.get("pydocstringformatter", None):
                    assert isinstance(pydocformat_sect, dict)
                    return pydocformat_sect
    return None


def parse_toml_option(  # pylint: disable=too-many-branches
    parser: argparse.ArgumentParser, opt: str, value: Any
) -> list[str]:
    """Parse an options value in the correct argument type for argparse."""
    # pylint: disable=protected-access
    try:
        action = parser._option_string_actions[f"--{opt}"]
    except KeyError as exc:
        try:
            action = parser._option_string_actions[f"-{opt}"]
        except KeyError:
            raise UnrecognizedOption(f"Don't recognize option {opt}") from exc

    if isinstance(action, BooleanOptionalAction):
        if not isinstance(value, bool):
            error_msg = f"{{'{value}'}} {type(value)} is not a supported argument for"
            error_msg += f" '{opt}', please use either {{true}} or {{false}}."
            raise ValueError(error_msg)

        if opt.startswith("no") and f"--{opt[3:]}" in action.option_strings:
            opposite_opt = opt[3:]
            val = ["false", "true"][value]
            opp_val = ["true", "false"][value]
            error_msg = (
                "TOML file contains an unsupported option "
                f"'{opt}: {val}', try using '{opposite_opt}: {opp_val}' instead"
            )
            raise TomlParsingError(error_msg)

        return [f"--{'no-' if not value else ''}{opt}"]

    if isinstance(action, argparse._StoreTrueAction):
        if value is True:
            return [action.option_strings[0]]
        return []

    if isinstance(action, argparse._StoreAction):
        if isinstance(value, int):
            value = str(value)
        return [action.option_strings[0], value]

    if isinstance(action, argparse._ExtendAction):
        out_args = []
        if isinstance(value, list):
            for item in value:
                out_args += [action.option_strings[0], item]
        else:
            out_args = [action.option_strings[0], value]

        return out_args

    raise NotImplementedError  # pragma: no cover


def parse_toml_file(
    parser: argparse.ArgumentParser, namespace: argparse.Namespace
) -> None:
    """Get and parse the relevant section form a pyproject.toml file."""
    if toml_sect := get_toml_file():
        arguments: list[str] = []

        for key, value in toml_sect.items():
            arguments += parse_toml_option(parser, key, value)

        parser.parse_args(arguments, namespace)
