"""Different mathematical operations done to signals.
"""
import numpy as np

def convolution(x, h, ylen_choice=True):
    """Perform a convolution operation with a filter h and a signal x.

    Arguments:
        x: An array representing a signal to be transformed.
        h: An array representing the FIR of a filter.
        y_choice: Whether to return a transformed signal of length
                  len(x) + len(h) + 1 (True, default), or of length len(x) (False).

    Return:
        y, and array representing the convolved signal.
    """
    return np.convolve(x, h, mode="full" if ylen_choice else "same")


def dtft(x, N=None, fs=1):
    """Discrete time Fourier transform a signal x.

    Arguments:
        x: An array representing a signal to be transformed.
        N: Number of points along the unit circle that are output for omega. 
           None by default, meaning the length of x is used.
        fs: The sampling frequency. 1 by default.

    Return:
        The complex valued array X(exp(j*omega)), and a tuple with a frequency 
        array and the real valued array with with amplitude for that frequency
    """
    if N is None:
        N = len(x)

    return np.fft.fft(x, N), (fs*np.arange(N)[::2], np.fft.rfft(x, N))
