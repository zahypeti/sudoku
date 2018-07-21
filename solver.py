"""
A custom class for efficiently solving a sudoku board.
"""
import numpy as np

EMPTY_DIGIT = -1


class Solver:

    def __init__(self, array):
        """
        Initialise this instance.

        Parameters
        ----------
        array: np.ndarray of ndim 2
            The 2D numpy array of np.int32 items representing the board.
            array[i][j] contains the integer representing the 0-based digit
            in that square, or EMPTY_DIGIT if it's empty.
        """
        if not isinstance(array, np.ndarray):
            msg = ('The {} class has to be instantiated with a '
                   'numpy.ndarray.').format(self.__class__.__name__)
            raise TypeError(msg)
