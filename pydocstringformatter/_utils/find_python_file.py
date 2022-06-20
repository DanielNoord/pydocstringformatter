from __future__ import annotations

import glob
import os
from pathlib import Path


def is_python_file(filename: str) -> bool:
    """Check if file is a Python file."""
    return filename.endswith(".py")


def find_python_files(
    filenames: list[str], exclude: list[str], recursive: bool = True
) -> list[Path]:
    """Find all python files for a list of potential file and directory names."""
    pathnames: list[Path] = []

    to_exclude: set[str] = set()
    for exclude_glob in exclude:
        to_exclude.update(set(glob.iglob(exclude_glob, recursive=recursive)))

    for name in filenames:
        if os.path.isdir(name):
            if recursive:
                for root, _, children in os.walk(name):
                    pathnames += [
                        Path(os.path.abspath(root)) / child
                        for child in children
                        if is_python_file(child)
                        and str(Path(root) / child) not in to_exclude
                    ]
            else:
                pathnames += [
                    file for file in Path(name).iterdir() if is_python_file(str(file))
                ]
        elif is_python_file(name):
            pathnames.append(Path(name))

    return sorted(pathnames)
