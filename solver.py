from copy import deepcopy

import numpy as np

from indexing import rows_cols, square
from operation import DIGIT_BOX, DIGIT_COLUMN, DIGIT_ROW, ROW_COLUMN
from operation_queue import OperationQueue

EMPTY_DIGIT = -1


class Solver:
    """
    A custom class for efficiently solving a sudoku board.
    """

    def __init__(self, array, box_height, box_width):
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

        # Constant attributes #################################################

        # The height and width of the box units
        self._box_height = box_height
        self._box_width = box_width

        # The side length of the sudoku board
        self._side_length = self._box_height * self._box_width

        # A single list over the coordinates of the squares in row-major order
        self._double_loop = [
            (i, j)
            for i in range(self._side_length)
            for j in range(self._side_length)]

        # Non-constant attributes #############################################

        # Main 3D data structure representing the current state of the board
        self.board = np.array(
            [[[True]
              * self._side_length] * self._side_length] * self._side_length,
            dtype=bool)

        # Solution steps to perform
        self.operations = OperationQueue(
            None, self._box_height, self._box_width)

    def secure(self, digit, row, col):
        pass

    def quick_fill(self):
        pass

    def _hidden_clash(self):
        pass

    def _first_empty_square(self):
        pass

    def recursively_solve(self):
        """
        Returns
        -------
        result : numpy.ndarray of ndim 2
            The solved board as a 2D numpy array. Digits are 0-based, and
            EMPTY_DIGIT items represent empty squares.

        Raises
        ------
        RunTimeError
            If it is found that the input board has no solutions.
        """
        pass

    def _update(self):
        pass
