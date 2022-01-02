import re
import tokenize


def _format_beginning_quotes(tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
    """Fix the position of the opening quotes"""
    new_string = tokeninfo.string
    if new_string[3] == "\n":
        new_string = re.sub(r"\n *", "", new_string, 1)
    return tokenize.TokenInfo(
        tokeninfo.type, new_string, tokeninfo.start, tokeninfo.end, tokeninfo.line
    )


def _format_multiline_ending_quotes(
    tokeninfo: tokenize.TokenInfo,
) -> tokenize.TokenInfo:
    """Fix the position of end quotes for multi-line docstrings"""
    good_end = f"{(tokeninfo.start[1]) * ' '}{(tokeninfo.string[0]) * 3}"
    new_string = tokeninfo.string
    split_string = new_string.split("\n")

    # Add new line with only quotes
    if not new_string.endswith("\n" + good_end):
        new_string = new_string[:-3] + "\n" + good_end
    # Remove line with only quotes for potential single line string
    elif len(split_string) == 2 and split_string[-1] == good_end:
        new_string = "\n".join(split_string[:-1]) + tokeninfo.string[0] * 3

    return tokenize.TokenInfo(
        tokeninfo.type, new_string, tokeninfo.start, tokeninfo.end, tokeninfo.line
    )


def _format_closing_quotes(tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
    """Fix the position of the closing quotes"""
    if "\n" in tokeninfo.string:
        return _format_multiline_ending_quotes(tokeninfo)
    return tokeninfo
