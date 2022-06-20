from __future__ import annotations

from collections.abc import Callable
from typing import Final, List


def comma_separated_list_validator(value: str | list[str]) -> list[str]:
    """Validate a comma separated list."""
    if isinstance(value, list):
        return value
    return value.split(",")


ValidatedTypes = List[str]
VALIDATORS: Final[dict[str, Callable[[str], ValidatedTypes]]] = {
    "csv": comma_separated_list_validator
}
