from typing import Callable, Dict, Final, List, Union


def _comma_separated_list_validator(value: Union[str, List[str]]) -> List[str]:
    """Validate a comma separated list."""
    if isinstance(value, list):
        return value
    return value.split(",")


ValidatedTypes = List[str]
VALIDATORS: Final[Dict[str, Callable[[str], ValidatedTypes]]] = {
    "csv": _comma_separated_list_validator
}
