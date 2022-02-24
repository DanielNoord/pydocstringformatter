def func():
    """
    a docstring"""

    def inner_func():
        """
        a docstring"""


def func(named_parameter: str) -> None:
    """'named_parameter' should have a nice name

    Other information here
    """
    print(named_parameter)


def func():
    """
    a multi-line
    docstring
    """

    def inner_func():
        """a multi-line
        docstring"""
