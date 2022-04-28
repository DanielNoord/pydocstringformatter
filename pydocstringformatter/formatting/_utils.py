def is_rst_title(summary: str) -> bool:
    """Check if the second line of a summary is one recurring character."""
    # If second line is one recurring character we're dealing with a rst title
    last_line = summary.splitlines()[-1].lstrip()
    return last_line.count(last_line[0]) == len(last_line)
