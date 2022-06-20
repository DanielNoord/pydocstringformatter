import difflib


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
