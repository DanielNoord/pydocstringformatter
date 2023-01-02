from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from pathlib import Path

import git

from pydocstringformatter._testutils.primer.const import PRIMER_DIRECTORY_PATH


@dataclass
class PackageToPrime:
    """Represents data about a package to be tested during primer tests."""

    url: str
    """URL of the repository to clone."""

    branch: str
    """Branch of the repository to clone."""

    directories: list[str]
    """Directories within the repository to run the program over."""

    arguments: list[str]
    """List of arguments to pass when priming the package."""

    @property
    def clone_directory(self) -> Path:
        """Directory to clone repository into."""
        clone_name = "/".join(self.url.split("/")[-2:]).replace(".git", "")
        return PRIMER_DIRECTORY_PATH / clone_name

    @property
    def paths_to_lint(self) -> list[str]:
        """The paths we need to run against."""
        return [str(self.clone_directory / path) for path in self.directories]

    def lazy_clone(self) -> None:
        """Clone the repo or pull any new commits.

        # TODO(#80): Allow re-using an already cloned repistory instead of removing it
        Currently this is therefore not really 'lazy'.
        """
        logging.info("Lazy cloning %s", self.url)

        if self.clone_directory.exists():
            shutil.rmtree(self.clone_directory)

        options: dict[str, str | int] = {
            "url": self.url,
            "to_path": str(self.clone_directory),
            "branch": self.branch,
            "depth": 1,
        }
        git.Repo.clone_from(**options)


PACKAGES = {
    "adventofcode": PackageToPrime(
        "https://github.com/DanielNoord/adventofcode",
        "main",
        ["."],
        [],
    ),
    "ProjectInventarisGezantschappen": PackageToPrime(
        "https://github.com/DanielNoord/ProjectInventarisGezantschappen",
        "main",
        ["python"],
        [],
    ),
    "pylint": PackageToPrime(
        "https://github.com/PyCQA/pylint",
        "main",
        ["pylint"],
        ["--max-summary-lines=2"],
    ),
    "pydocstringformatter": PackageToPrime(
        "https://github.com/DanielNoord/pydocstringformatter",
        "main",
        ["pydocstringformatter"],
        [],
    ),
    "pylint-pytest-plugin": PackageToPrime(
        "https://github.com/DanielNoord/pylint-pytest-plugin",
        "main",
        ["pylint_pytest_plugin"],
        ["--linewrap-full-docstring"],
    ),
}
