import token
import tokenize

PREVIOUS_TOKEN_MARKERS = (token.INDENT, token.ENDMARKER, token.NEWLINE)


def is_docstring(
    tokeninfo: tokenize.TokenInfo, previous_token: tokenize.TokenInfo
) -> bool:
    """Check if a token represents a docstring."""
    if (
        tokeninfo.type == token.STRING
        and (
            previous_token.type in PREVIOUS_TOKEN_MARKERS
            or previous_token.type == token.NL
            and not tokeninfo.start[1]
        )
        and tokeninfo.line.strip().startswith(("'", '"'))
    ):
        return True
    return False
