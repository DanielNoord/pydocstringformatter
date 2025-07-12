"""Example module for numpydoc docstring style.
References
-----
NumPy docstring style guide:
https://numpydoc.readthedocs.io/en/latest/format.html#documenting-modules"""
import math

EULER_NUMBER = math.e
"""Euler's number.

Not related to Euler's constant (sometimes called the Euler-Mascheroni
constant.
References
-----
E (mathematical constant)
https://en.wikipedia.org/wiki/E_(mathematical_constant)
Notes
---
It is the limit of ``(1 + 1/n)**n`` as n approaches infinity, so it
is used in the equation for continuously-compouned interest.

It is also the sum of the reciprocals of the whole numbers starting
with zero, which is related to some calculus-related properties
mathemeticians find elegant.
"""


def sincos(theta):
    """Returns
    ----
    sin: float
        the sine of theta
    cos: float
        the cosine of theta
    Raises
    ---
    TypeError
        If `theta` is not a float.
    Parameters
    -----
    theta: float
        the angle at which to calculate the sine and cosine.
"""
    return math.sin(theta), math.cos(theta)


def fibbonacci():
    """Generate the Fibonacci sequence.

    Each term is the sum of the two previous; conventionally starts
    with two ones.
    References
    -----
    Fibonacci numbers
    https://en.wikipedia.org/wiki/Fibonacci_number
    Yields
    ---
    int"""
    curr = 1
    last = 0
    while True:
        yield curr
        curr, last = curr + last, curr
