from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pydocstringformatter._testutils.primer.const import DIFF_OUTPUT
from pydocstringformatter._testutils.primer.packages import PACKAGES, PackageToPrime


def fix_diff(output: str, package: PackageToPrime) -> str:
    """Make the diff more readable and useful."""
    new_output: list[str] = []

    for index, line in enumerate(output.splitlines()):
        if line.startswith("--- "):
            if index:
                new_output.append("```\n")

            link = line.replace("--- ../.pydocstringformatter_primer_tests/", "")
            file = "/".join(link.split("/")[2:])

            new_output.append(f"{package.url}/blob/{package.branch}/{file}")
            new_output.append("```diff")

        new_output.append(line)

    return "\n".join(new_output)


def run_prepare() -> None:
    """Prepare everything for the primer to be run.

    This clones all packages that need to be 'primed' and
    does any other necessary setup.
    """
    for package in PACKAGES.values():
        package.lazy_clone()

    print("## Preparation of primer successful!")


def run_step_one() -> None:
    """Run program over all packages in write mode.

    Runs the program in write mode over all packages that need
    to be 'primed'. This should be run when the local repository
    is checked out to upstream/main.
    """
    for package in PACKAGES.values():
        subprocess.run(
            [sys.executable, "-m", "pydocstringformatter", "-w"]
            + package.paths_to_lint
            + package.arguments,
            cwd=Path(__file__).parent.parent.parent,
            capture_output=True,
            text=True,
            check=False,
        )

    print("## Step one of primer successful!")


def run_step_two() -> None:
    """Run program over all packages and store the diff.

    This reiterates over all packages that need to be 'primed',
    runs the program in diff mode and stores the output to file.
    """
    output: dict[str, str] = {}

    for name, package in PACKAGES.items():
        process = subprocess.run(
            [sys.executable, "-m", "pydocstringformatter"]
            + package.paths_to_lint
            + package.arguments,
            cwd=Path(__file__).parent.parent.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        output[name] = fix_diff(process.stdout, package)

    final_output = ""
    for name, string in output.items():
        if string.startswith("Nothing to do!"):
            continue
        final_output += f"**{name}:**\n\n{string}\n\n"

    with open(DIFF_OUTPUT, "w", encoding="utf-8") as file:
        file.write(final_output)

    print("## Step two of primer successful!")


def run_primer() -> None:
    """Run the primer test."""
    args = sys.argv[1:]

    if "--prepare" in args:
        run_prepare()
    elif "--step-one" in args:
        run_step_one()
    elif "--step-two" in args:
        run_step_two()


if __name__ == "__main__":
    run_primer()
