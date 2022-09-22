import difflib
import tokenize

from pydocstringformatter._formatting import Formatter


def generate_diff(old: str, new: str, filename: str) -> str:
    """Generate a printable diff for two strings of sourcecode."""
    return (
        "\n".join(
            difflib.unified_diff(
                old.split("\n"),
                new.split("\n"),
                fromfile=filename,
                tofile=filename,
                lineterm="",
            )
        )
        + "\n"
    )


def compare_formatters(
    token: tokenize.TokenInfo,
    formatter_1: Formatter,
    formatter_2: Formatter,
    title_extra: str = "",
) -> str:
    """Modifies a token with two formatters and returns the difference."""
    out_t1 = formatter_1.treat_token(token)
    out_t2 = formatter_2.treat_token(out_t1)

    title = f"{formatter_1.name} vs {formatter_2.name}"
    if title_extra:
        title += f" {title_extra}"
    return generate_diff(out_t1.string, out_t2.string, title)
