from copy import deepcopy
from math import sqrt
import string

import numpy as np

from indexing import rows_cols, square
from operation import DIGIT_BOX, DIGIT_COLUMN, DIGIT_ROW, ROW_COLUMN
from operation_queue import OperationQueue


class Board:
    """
    Object that holds the state of a sudoku board (of a fixed size) and
    provides methods for filling in some squares and solving it completely.
    """

    def __init__(self, *args):
        """
        Set up an empty board of a given size. To populate the board, use the
        from_str() method instead.

        Parameters
        ----------
        size : int or 2-tuple of ints
            If a single argument is given, the board is created with the
            given argument as its side length. Default is 9.
            If two arguments are given, the board is created with the given
            box height and width.
        """

        # Parse arguments and set box height and width
        if len(args) == 0:
            # Default is a 9x9 board
            self._box_height = 3
            self._box_width = 3

        elif len(args) == 1:

            # Assume a square shaped board if a single argument is provided
            side_length = args[0]
            # Raise error if it's not a square number
            if side_length != int(sqrt(side_length))**2:
                msg = 'The side length of the board must be a square number.'
                raise ValueError(msg)

            # The given argument corresponds to the side length
            self._box_height = int(sqrt(side_length))
            self._box_width = int(sqrt(side_length))

        elif len(args) == 2:
            self._box_height = args[0]
            self._box_width = args[1]

        else:
            raise ValueError('Too many arguments.')

        # Constant properties #################################################

        # The side length of the sudoku board
        self._side_length = self._box_height * self._box_width
        # Raise an error if characters would run out due to a large board size
        if 37 <= self._side_length:
            msg = 'The side length of the board must be less than 37.'
            raise ValueError(msg)

        # An iterator for the coordinates of all the squares
        self._double_loop = [
            (i, j)
            for i in range(self._side_length)
            for j in range(self._side_length)]

        # Create the string containing all possible digits up to base 36
        base36digits = string.digits + string.ascii_uppercase
        # The characters used for digit representation (1-based indexing)
        self._alphabet = base36digits[1:self._side_length+1]

        # Auxiliary attributes ################################################

        # Main 3D data structure representing the current state of the board
        self._board = np.array(
            [[[True]
              * self._side_length] * self._side_length] * self._side_length,
            dtype=bool)

        # Solution steps to perform
        self._operations = OperationQueue(
            None, self._box_height, self._box_width)

        # Public attributes ###################################################

        # Number of empty squares at any point in time
        self.empties = self._side_length ** 2

    def __str__(self):
        result = ''
        for row, col in self._double_loop:
            candidates = self._board[:, row, col].nonzero()[0]
            if len(candidates) == 1:
                result += self._alphabet[candidates[0]]
            else:
                result += '.'
            if col == self._side_length - 1:
                result += '\n'
        return result

    def __repr__(self):
        return f'Board({self._box_height}, {self._box_width})'

    def _add(self, digit, row, col):
        """
        Make digit the only candidate in the given square, if possible.
        
        To be used as the primary interface that directly modifies this class
        object (beside _update).

        Parameters
        ----------
        digit : int
            The digit with which the given square is to be filled in.
            0-based indexing, i.e. should be in range(_size_length).
        row : int
            The particular square's row index. 0-based indexing, i.e. should be
            in range(_size_length).
        col : int
            The particular square's row index. 0-based indexing, i.e. should be
            in range(_size_length).
        
        Raises
        ------
        ValueError
            If digit is already a candidate at the given position.
        """

        # Check if digit is actually a candidate in the given square
        if not self._board[digit, row, col]:
            # return
            raise ValueError(
                f'[_add({digit}, {row}, {col})] '
                f'{digit+1} is not a candidate at ({row+1},{col+1})'
            )

        # Remove peer candidates
        row_slice, col_slice = rows_cols(row, col,
                                         self._box_height, self._box_width)

        self._board[:, row, col] = [False] * self._side_length
        self._board[digit, row, :] = [False] * self._side_length
        self._board[digit, :, col] = [False] * self._side_length
        self._board[digit:digit+1, row_slice, col_slice] = (
                [[False] * self._box_width] * self._box_height
        )

        # Make this a digit in the square
        self._board[digit, row, col] = True

        # Update attributes
        self._operations.remove_rearrange(digit, row, col)
        self.empties -= 1

    def from_str(self, lst):
        """
        Build the board from the given character representation.
        Digits are interpreted using 1-based indexing, and '.' & '0' represent
        blank squares.

        Parameters
        ----------
        lst : iterable of characters

        Returns
        -------
        success : bool
            Whether the input was valid with a board that does not have
            immediate clash.
        """
        self.__init__(self._box_height, self._box_width)
        i = 0
        for row, col in self._double_loop:
            char = lst[i]
            if char in self._alphabet or char == '.':
                if char == '.' or char == '0':
                    pass
                else:
                    digit = int(char, base=36) - 1
                    if self._board[digit, row, col]:
                        self._add(digit, row, col)
                    else:
                        msg = f"Clash found at ({row+1}, {col+1})"
                        print(msg)
                        self.__init__(self._box_height, self._box_width)
                        return False
            i += 1
        return True
        
    def quick_fill(self):
        """
        Fill in the obvious digits in place.
        
        Returns
        -------
        success : bool
            False if detects immediate clash during the process, True otherwise.
        """

        # repeat this until no new entry, FIXME 30 Mar 2018
        niter = -1
        while not self._operations.empty() and niter < 400:
            niter += 1
            operation = self._operations.get_head()
            i, j = operation.indices
            digit = row = col = None

            if operation.inspects == ROW_COLUMN:
                # Find squares with unique digits
                row, col = i, j
                candidates = self._board[:, row, col].nonzero()[0]
                if len(candidates) == 1:
                    digit = candidates[0]

            elif operation.inspects == DIGIT_ROW:
                # Find row & digit that has unique column
                digit, row = i, j
                positions = self._board[digit, row, :].nonzero()[0]
                if len(positions) == 1:
                    col = positions[0]

            elif operation.inspects == DIGIT_COLUMN:
                # Find col & digit that has unique row
                digit, col = i, j
                positions = self._board[digit, :, col].nonzero()[0]
                if len(positions) == 1:
                    row = positions[0]

            elif operation.inspects == DIGIT_BOX:
                # Find box & digit that has unique position within box
                digit, box = i, j
                row_slice, col_slice = \
                    rows_cols(box, self._box_height, self._box_width)
                subarray_2d = self._board[digit, row_slice, col_slice]

                # Make the 2D array one dimensional (in row-major order)
                positions = subarray_2d.flatten('C').nonzero()[0]
                if len(positions) == 1:
                    position = positions[0]
                    row, col = square(box, position,
                                      self._box_height, self._box_width)

            if digit and row and col:
                self._add(digit, row, col)
            else:
                self._operations.requeue()

        return True

    def _hidden_clash(self):
        """
        Return False if all squares have at least one possible candidate,
        otherwise return the position of the first found.
        """
        
        for i, j in self._double_loop:
            if len(self._board[:, i, j].nonzero()[0]) == 0:
                return i, j
        
        return False
        
    def _first_empty_square(self):
        """
        Find an empty square to be filled in and return its coordinates.
        """
        
        for row, col in self._double_loop:
            if len(self._board[:, row, col].nonzero()[0]) > 1:
                return row, col
        
        return None, None

    def solve(self):
        success, depth = self._recursively_solve()
        return success

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
            msg = 'Clash found during the solution of the board.'
            print(msg)
            return False, depth
        
        # Check if finished, FIXME
        
        # Check if there are no-candidate squares
        tpl = self._hidden_clash()
        if tpl:
            msg = (f'Hidden clash found during the solution of the board at '
                   f'{tpl}')
            print(msg)
            return False, depth
        
        # Find a square not yet filled
        row, column = self._first_empty_square()
        if row is None and column is None:
            # No empty cells
            return True, depth
        
        # Put most probable candidate first, FIXME 30 Mar
        candidate_digits = sorted(self._board[:, row, column].nonzero()[0])
        
        # Recursively call this method with one new entry
        for digit in candidate_digits:
            # Add the candidate digit to the child
            child = deepcopy(self)
            child._add(digit, row, column)

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
        msg = 'No solution exists.'
        print(msg)
        return False, depth
    
    def _update(self, obj):
        """
        Update nonzero (filled in) squares from the board attribute of obj.
        """
        
        for i, j in self._double_loop:
            candidates = obj._board[:, i, j].nonzero()[0]
            if len(candidates) == 1:
                digit = candidates[0]
                self._add(digit, i, j)
