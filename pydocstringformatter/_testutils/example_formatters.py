import tokenize

from pydocstringformatter._formatting import Formatter


class MakeAFormatter(Formatter):
    """A formatter that makes Bs into As."""

    name = "make-a-formatter"
    style = ["default"]

    def treat_token(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        """Replace Bs with As."""
        token_dict = tokeninfo._asdict()
        token_dict["string"] = token_dict["string"].replace("B", "A")
        return type(tokeninfo)(**token_dict)


class MakeBFormatter(Formatter):
    """A formatter that makes As into Bs."""

    name = "make-b-formatter"
    style = ["default"]

    def treat_token(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        """Replace As with Bs."""
        token_dict = tokeninfo._asdict()
        token_dict["string"] = token_dict["string"].replace("A", "B")
        return type(tokeninfo)(**token_dict)


class AddBFormatter(Formatter):
    """A formatter that adds Bs."""

    name = "add-b-formatter"
    style = ["default"]

    def treat_token(self, tokeninfo: tokenize.TokenInfo) -> tokenize.TokenInfo:
        """Add a B to the end of the string."""
        token_dict = tokeninfo._asdict()
        token_dict["string"] += "B"
        return type(tokeninfo)(**token_dict)
