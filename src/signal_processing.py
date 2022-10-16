"""Different mathematical operations done to signals.
"""
import numpy as np

def convolution(x, h, y_choice=True):
    """Perform a convolution operation with a filter h and a signal x.

    Arguments:
        x: An array representing a signal to be transformed.
        h: An array representing the FIR of a filter.
        y_choice: Whether to return a transformed signal of length
                  len(x) + len(h) + 1 (True, default), or of length len(x) (False).

    Return:
        y, and array representing the convolved signal.
    """
    return np.convolve(x, h, mode=="full" is y_choice else "same")
