import re
import tokenize


def _format_beginning_quotes(tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
    """Fix the position if the opening quotes"""
    new_string = tokeninfo.string
    if new_string[3] == "\n":
        new_string = re.sub(r"\n *", "", new_string, 1)
    return tokenize.TokenInfo(
        tokeninfo.type, new_string, tokeninfo.start, tokeninfo.end, tokeninfo.line
    )


def _format_multiline_quotes(tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
    """Fix the position of end quotes for multi-line docstrings"""
    good_end = f"\n{(tokeninfo.start[1]) * ' '}{(tokeninfo.string[0]) * 3}"
    new_string = tokeninfo.string
    if not new_string.endswith(good_end):
        new_string = new_string[:-3] + good_end
    return tokenize.TokenInfo(
        tokeninfo.type, new_string, tokeninfo.start, tokeninfo.end, tokeninfo.line
    )
