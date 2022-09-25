from __future__ import annotations

import tokenize

from pydocstringformatter._formatting import Formatter
from pydocstringformatter._utils.file_diference import compare_formatters


def create_gh_issue_template(
    token: tokenize.TokenInfo, formatters: dict[str, Formatter], filename: str
) -> str:
    """Make a template for a GitHub issue.

    Args:
        token: The token that caused the issue.
        formatters: The formatters that caused the issue.
        filename: The filename of the file that caused the issue.
    """
    formatter_names = list(formatters)
    msg = ""
    if len(formatter_names) > 2:
        msg = f"""
Conflicting formatters: {", ".join(formatters)}
"""
        diff = f"Diff too intricate to compute for {len(formatter_names)} formatters."
    else:
        if len(formatter_names) == 2:
            msg = f"""
Conflicting formatters: {" and ".join(formatter_names)}
These formatters conflict with each other for:

```python
{token.string}
```
"""
            formatter_1 = formatters[formatter_names[0]]
            formatter_2 = formatters[formatter_names[1]]
        else:
            msg = f"""
Formatter: {formatter_names[0]}
This formatter is not able to make stable changes for:

```python
{token.string}
```
"""
            formatter_1 = formatters[formatter_names[0]]
            formatter_2 = formatter_1

        diff = compare_formatters(
            token,
            formatter_1,
            formatter_2,
            title_extra=str(filename),
        )

    out = f"""
Unfortunately an error occurred while formatting a docstring.
Please help us fix this bug by opening an issue at:
https://github.com/DanielNoord/pydocstringformatter/issues/new

{"-" * 80}

You can use the following template when you open the issue:

# Description:

{msg}

# Diff:

```diff
{diff}
```

"""

    return out
