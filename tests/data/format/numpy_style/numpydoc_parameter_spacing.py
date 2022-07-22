import math

def sincos(theta):
    """Calculate the sine and cosine of theta.

    Parameters
    ----------
    theta: float
        the angle at which to calculate the sine and cosine.

    Returns
    -------
    sin: float
        the sine of theta
    cos: float
        the cosine of theta

    Raises
    ------
    TypeError
        If `theta` is not a float.
    """
    return math.sin(theta), math.cos(theta)
