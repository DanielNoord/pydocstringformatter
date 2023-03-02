[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pydocstringformatter.svg)](https://pypi.python.org/pypi/pydocstringformatter/)
[![codecov](https://codecov.io/gh/DanielNoord/pydocstringformatter/branch/main/graph/badge.svg?token=TR61QNMBZG)](https://codecov.io/gh/DanielNoord/pydocstringformatter)
[![Tests](https://github.com/DanielNoord/pydocstringformatter/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/DanielNoord/pydocstringformatter/actions/workflows/tests.yaml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DanielNoord/pydocstringformatter/main.svg)](https://results.pre-commit.ci/latest/github/DanielNoord/pydocstringformatter/main)
[![Documentation Status](https://readthedocs.org/projects/pydocstringformatter/badge/?version=latest)](https://pydocstringformatter.readthedocs.io/en/latest/?badge=latest)

# Pydocstringformatter

A tool to automatically format Python docstrings to follow recommendations from
[`PEP 8`](https://www.python.org/dev/peps/pep-0008/) and
[`PEP 257`](https://www.python.org/dev/peps/pep-0257/) (or other supported style
guides.)

See [What it does](#what-it-does) for currently supported auto-formatting.

**Rationale**

This project is heavily inspired by
[`docformatter`](https://github.com/PyCQA/docformatter).

When this project was started `docformatter` did not meet all of the requirements the
[`pylint`](https://github.com/PyCQA/pylint) project had for its docstring formatter and
was no longer actively maintained (this has changed since then). Therefore, some
contributors of `pylint` got together and started working on our own formatter to
fulfill our needs.

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
strip-whitespaces = true
split-summary-body = false
numpydoc-section-hyphen-length = false
```

#### Style

Pydocstringformatter can be configured to use a specific style. The default is `pep257`
but we support other styles as well. These can also be used at the same time. For
example with:

```console
pydocstringformatter --style=pep257 --style=numpydoc myfile.py
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

The following examples show some of the changes pydocstringformatter will apply. For a
full overview of all potential changes you can check out the
[`Usage`](https://pydocstringformatter.readthedocs.io/en/latest/usage.html) page which
shows an up to date list of all formatters and their description.

```python
# Bad
'''
my docstring'''

"""    my
multi-line docstring      """

"""my title
===========

my docstring
"""


# Good
"""My docstring."""

"""My
multi-line docstring.
"""

"""My title
===========

My docstring
"""

# With --summary-quotes-same-line
# Bad
"""
My
multi-line docstring
"""

# Good
"""My
multi-line docstring
"""
```

## Development

For development and contributing guidelines please see
[`Development`](https://pydocstringformatter.readthedocs.io/en/latest/development.html).
