import argparse
from typing import List


def _parse_command_line_arguments(
    parser: argparse.ArgumentParser, namespace: argparse.Namespace, args: List[str]
) -> None:
    """Parse all arguments on the provided argument parser."""
    parser.parse_known_args(args, namespace)
