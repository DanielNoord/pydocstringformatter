[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pydocstringformatter.svg)](https://pypi.python.org/pypi/pydocstringformatter/)
[![Coverage Status](https://coveralls.io/repos/github/DanielNoord/pydocstringformatter/badge.svg?branch=main)](https://coveralls.io/github/DanielNoord/pydocstringformatter?branch=main)
[![Tests](https://github.com/DanielNoord/pydocstringformatter/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/DanielNoord/pydocstringformatter/actions/workflows/tests.yaml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DanielNoord/pydocstringformatter/main.svg)](https://results.pre-commit.ci/latest/github/DanielNoord/pydocstringformatter/main)
[![Documentation Status](https://readthedocs.org/projects/pydocstringformatter/badge/?version=latest)](https://pydocstringformatter.readthedocs.io/en/latest/?badge=latest)

# Pydocstringformatter

A tool to automatically format Python docstrings to follow recommendations from
[`PEP 8`](https://www.python.org/dev/peps/pep-0008/) and
[`PEP 257`](https://www.python.org/dev/peps/pep-0257/).

See [What it does](#what-it-does) for currently supported auto-formatting.

### Rationale

This project is heavily inspired by
[`docformatter`](https://github.com/PyCQA/docformatter).

When this project was started `docformatter` did not meet all of the requirements the
[`pylint`](https://github.com/PyCQA/pylint) project had for its docstring formatter and
sadly `docformatter` is now also no longer fully supported. Therefore, some contributors
of `pylint` got together and started working on our own formatter to fulfill our needs.

When asked we defined the objective of the tool as:

_"A docstring formatter that follows PEP8 and PEP257 but makes some of the more
'controversial' elements of the PEPs optional"_

See
[the original answer](https://github.com/DanielNoord/pydocstringformatter/issues/38).

As such, the biggest difference between the two is that `pydocstringformatter` fixes
some of the open issues we found in `docformatter`. In general, the output of both
formatters (and any other docstring formatter) should be relatively similar.

## How to install

```shell
pip install pydocstringformatter
```

## Usage

[`Click here`](https://pydocstringformatter.readthedocs.io/en/latest/usage.html) for a
full Usage overview.

```shell
usage: pydocstringformatter [-h] [-w] [--exclude EXCLUDE] [-v] [files ...]

positional arguments:
  files                 The directory or files to format.

options:
  -h, --help            show this help message and exit
  -w, --write           Write the changes to file instead of printing the diffs to stdout.
  --quiet               Do not print any logging or status messages to stdout.
  -v, --version         Show version number and exit.
  --max-line-length     The maximum docstring line length. Default set to 88.

configuration:
  --exclude EXCLUDE     A comma separated list of glob patterns of file path names not to be formatted.
```

### Configuration

Pydocstringformatter will also read any configuration added to the
`[tool.pydocstringformatter]` section of a `pyproject.toml` file.

For example:

```toml
[tool.pydocstringformatter]
write = true
exclude = "**/my_dir/**,**/my_other_dir/**"
# Or:
exclude = ["**/my_dir/**", "**/my_other_dir/**"]
```

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

**PEP 257: _The closing quotes are on the same line as the opening quotes_**

This can be enforced on multi-line docstrings with the `--summary-quotes-same-line`
option. This behaviour is turned off by default.

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

# With --summary-quotes-same-line
"""
My
multi-line docstring
"""

# Good
"""My docstring"""

"""My docstring"""

"""
My
multi-line docstring
"""

# With --summary-quotes-same-line
"""My
multi-line docstring
"""
```

**PEP 257: _The docstring is a phrase ending in a period & Multi-line docstrings consist
of a summary line just like a one-line docstring_**

Since the first line should be a phrase or summary the first character gets capitalized.

When the second line is one recurring character we consider the summary line to be a
title as used in many Sphinx documentation schemes and do not add a period.

```python
# Bad
"""my docstring"""

"""
summary

my docstring
"""


# Good
"""My docstring."""

"""
Summary.

my docstring
"""

"""My title
===========

My docstring
"""
```

**PEP 257: _Multi-line docstrings consist of a summary line just like a one-line
docstring, followed by a blank line, followed by a more elaborate description._**

When the second line is one recurring character we consider the summary line to be a
title as used in many Sphinx documentation schemes and do not add a white line.

```python
# Bad
"""Summary. Body."""

"""Summary.
Body.
"""

# Good
"""Summary.

Body.
"""

"""My title
===========

My docstring
"""
```

**PEP 257: _For consistency, always use """triple double quotes""" around docstrings._**

```python
# Bad
"My docstring"

'My docstring'

'''My docstring'''

'''Summary.

Body.
'''

# Good
"""My docstring"""

"""My docstring"""

"""My docstring"""

"""Summary.

Body.
"""
```

**_Trailing or leading whitespaces get removed as well._**

```python
# Bad
"""  My docstring.  """

"""  Summary.

Body
  """

"""  My docstring.

    My indented section
"""

# Good
"""My docstring."""

"""  Summary.

Body
"""

"""My docstring.

    My indented section
"""
```

## Development

For development and contributing guidelines please see
[`Development`](https://pydocstringformatter.readthedocs.io/en/latest/development.html).
