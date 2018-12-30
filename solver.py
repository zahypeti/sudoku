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
        """
        Make digit the only candidate in the given square, if possible.

        To be used as the primary interface that directly modifies this class
        object (beside _update).

        Parameters
        ----------
        digit : int
            The digit with which the given square is to be filled in.
            Assumes 0-based indexing, so should be in range(_size_length).
            Also, use ints even if the string representation is 'B' for
            instance.
        row : int
            The particular square's row index. Assumes 0-based indexing,
            so should be in range(_size_length).
        col : int
            The particular square's column index. Assumes 0-based indexing,
            so should be in range(_size_length).

        Raises
        ------
        ValueError
            If digit is not a possible candidate at the given position.
        """

        # Check if digit is actually a candidate in the given square
        if not self.board[digit, row, col]:
            msg = '[_add({}, {}, {})]'.format(digit, row, col)
            print(msg)
            raise ValueError(
                '{} is not a candidate at ({},{})'.format(
                    digit+1, row+1, col+1))

        # Remove peer candidates
        row_slice, col_slice = rows_cols(row, col,
                                         self._box_height, self._box_width)

        self.board[:, row, col] = [False] * self._side_length
        self.board[digit, row, :] = [False] * self._side_length
        self.board[digit, :, col] = [False] * self._side_length
        self.board[digit:digit+1, row_slice, col_slice] = (
                [[False] * self._box_width] * self._box_height
        )

        # Make this a digit in the square
        self.board[digit, row, col] = True

        # Update attributes
        self.operations.remove_rearrange(digit, row, col)

    def quick_fill(self):
        """
        Fill in the obvious digits in place.

        Returns
        -------
        success : bool
            False if detects immediate clash during the process, and True
            otherwise.
        """

        # repeat this until no new entry, FIXME 30 Mar 2018
        niter = -1
        while not self.operations.empty() and niter < 400:
            niter += 1
            operation = self.operations.get_head()
            i, j = operation.indices
            digit = row = col = None

            if operation.inspects == ROW_COLUMN:
                # Find squares with unique digits
                row, col = i, j
                candidates = self.board[:, row, col].nonzero()[0]
                if len(candidates) == 1:
                    digit = candidates[0]

            elif operation.inspects == DIGIT_ROW:
                # Find row & digit that has unique column
                digit, row = i, j
                positions = self.board[digit, row, :].nonzero()[0]
                if len(positions) == 1:
                    col = positions[0]

            elif operation.inspects == DIGIT_COLUMN:
                # Find col & digit that has unique row
                digit, col = i, j
                positions = self.board[digit, :, col].nonzero()[0]
                if len(positions) == 1:
                    row = positions[0]

            elif operation.inspects == DIGIT_BOX:
                # Find box & digit that has unique position within box
                digit, box = i, j
                row_slice, col_slice = \
                    rows_cols(box, self._box_height, self._box_width)
                subarray_2d = self.board[digit, row_slice, col_slice]

                # Make the 2D array one dimensional (in row-major order)
                positions = subarray_2d.flatten('C').nonzero()[0]
                if len(positions) == 1:
                    position = positions[0]
                    row, col = square(box, position,
                                      self._box_height, self._box_width)

            if digit is not None and row is not None and col is not None:
                self.secure(digit, row, col)
            else:
                self.operations.requeue()

        return True

    def _hidden_clash(self):
        """
        Return False if all squares have at least one possible candidate,
        otherwise return the position of the first found.
        """

        for i, j in self._double_loop:
            if len(self.board[:, i, j].nonzero()[0]) == 0:
                return i, j

        return False

    def _first_empty_square(self):
        """
        Find an empty square to be filled in and return its coordinates.
        """

        for row, col in self._double_loop:
            if len(self.board[:, row, col].nonzero()[0]) > 1:
                return row, col

        return None, None

    def _recursively_solve(self):
        """
        Find the "first" solution recursively and using quick_fill().

        Find an empty square, try all possible candidates, and solve each new
        board recursively until first solution found.

        Returns
        -------
        success : bool
            True if solution found, False when clash occurs.
        depth : int
            Recursion depth - the number of times the method calls itself.
            Zero if the first quick_fill() solves the board immediately.
        """

        depth = 0

        # Fill in obvious squares in place before recursion

        success = self.quick_fill()
        if not success:
            # Clash found during the solution of the board
            return False, depth

        # Check if finished, FIXME

        # Check if there are no-candidate squares
        tpl = self._hidden_clash()
        if tpl:
            # Hidden clash found during the solution of the board at tpl
            return False, depth

        # Find a square not yet filled
        row, column = self._first_empty_square()
        if row is None and column is None:
            # No empty cells
            return True, depth

        # Put most probable candidate first, FIXME 30 Mar
        candidate_digits = sorted(self.board[:, row, column].nonzero()[0])

        # Recursively call this method with one new entry
        for digit in candidate_digits:
            # Add the candidate digit to the child
            child = deepcopy(self)
            child.secure(digit, row, column)

            # Try solving with the new entry
            success, child_depth = child._recursively_solve()
            depth = child_depth + 1
            if not success:
                continue

            # Stop when the first solution is found
            if success:
                # Update self from the solved child
                self._update(child)
                return True, depth

        # None of the children lead to a solution
        # msg = 'No solution exists.'
        return False, depth

    def _update(self, obj):
        """
        Update nonzero (filled in) squares from the board attribute of obj.
        """

        for i, j in self._double_loop:
            candidates = obj.board[:, i, j].nonzero()[0]
            if len(candidates) == 1:
                digit = candidates[0]
                self.secure(digit, i, j)
