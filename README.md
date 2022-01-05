[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pydocstringformatter.svg)](https://pypi.python.org/pypi/pydocstringformatter/)
[![Coverage Status](https://coveralls.io/repos/github/DanielNoord/pydocstringformatter/badge.svg?branch=main)](https://coveralls.io/github/DanielNoord/pydocstringformatter?branch=main)
[![Tests](https://github.com/DanielNoord/pydocstringformatter/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/DanielNoord/pydocstringformatter/actions/workflows/tests.yaml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DanielNoord/pydocstringformatter/main.svg)](https://results.pre-commit.ci/latest/github/DanielNoord/pydocstringformatter/main)

# Pydocstringformatter

A tool to automatically format Python docstrings that tries to follow recommendations
from [`PEP 8`](https://www.python.org/dev/peps/pep-0008/) and
[`PEP 257`](https://www.python.org/dev/peps/pep-0257/). See
[What it does](#what-it-does) for currently supported auto-formatting.

## How to install

```shell
pip install pydocstringformatter
```

## Usage

```shell
usage: pydocstringformatter [-h] [-w] [-v] [files ...]

positional arguments:
  files

options:
  -h, --help     show this help message and exit
  -w, --write    Write the changes to file instead of printing the diffs to stdout
  -v, --version  Show version number and exit
```

### Configuration

Pydocstringformatter will also read any configuration added to the
`[tool.pydocstringformatter]` section of a `pyproject.toml` file.

## Pre-commit

Pydocstringformatter can also be used as a [pre-commit hook](https://pre-commit.com).
Add the following to your `.pre-commit-config.yaml` file:

```yaml
- repo: https://github.com/DanielNoord/pydocstringformatter
  rev: SPECIFY VERSION HERE
  hooks:
    - id: pydocstringformatter
```

## What it does

The following examples show what pydocstringformatter will pick up on. All _bad_
examples will be rewritten to follow the _good_ patterns.

**PEP 8: _Note that most importantly, the """ that ends a multiline docstring should be
on a line by itself:_**

```python
# Bad
"""My
multi-line docstring"""

# Good
"""My
multi-line docstring
"""
```

**PEP 256: _The closing quotes are on the same line as the opening quotes_**

For consistency this rule also gets applied to multi-line docstrings

```python
# Bad
"""
My docstring"""

"""My docstring
"""

"""
My
multi-line docstring
"""

# Good
"""My docstring"""

"""My docstring"""

"""My
multi-line docstring
"""
```

## Development

For development and contributing guidelines please see
[`Contributing`](https://github.com/DanielNoord/pydocstringformatter/blob/main/.github/CONTRIBUTING.md).
