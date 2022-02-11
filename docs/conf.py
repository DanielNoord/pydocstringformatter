# pylint: disable=invalid-name

"""Configuration file for the Sphinx documentation builder."""

# -- Path setup --------------------------------------------------------------

# Add parent directory so we can import pydocstringformatter
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# pylint: disable-next=import-error, wrong-import-position
import pydocstringformatter  # noqa: E402

# -- Project information -----------------------------------------------------

project = "pydocstringformatter"
copyright = "2022, Github Contributors"  # pylint: disable=redefined-builtin
author = "Github Contributors"
release = pydocstringformatter.__version__

# -- General configuration ---------------------------------------------------

extensions = ["myst_parser"]
source_suffix = [".rst", ".md"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_theme_options = {
    # pylint: disable-next=line-too-long
    "description": "A tool to automatically format Python docstrings that tries to follow recommendations from PEP 8 and PEP 257.",  # noqa: E501
    "donate_url": "https://github.com/DanielNoord/pydocstringformatter",
    "github_repo": "pydocstringformatter",
    "github_user": "DanielNoord",
    "fixed_sidebar": True,
}

html_static_path = ["_static"]
