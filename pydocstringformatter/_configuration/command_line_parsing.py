from __future__ import annotations

import argparse


def parse_command_line_arguments(
    parser: argparse.ArgumentParser, namespace: argparse.Namespace, args: list[str]
) -> None:
    """Parse all arguments on the provided argument parser."""
    parser.parse_known_args(args, namespace)
