from copy import deepcopy
from math import sqrt
import numpy as np

from indexing import rows_cols, square
from operation_queue import OperationQueue


class Board:

    def __init__(self, *args):
        
        # Board size
        if len(args) == 0:
            self._box_height = 3
            self._box_width = 3
        elif len(args) == 1:
            # Assume square box
            side_length = args[0]
            self._box_height = int(sqrt(side_length))
            self._box_width = int(sqrt(side_length))
        elif len(args) == 2:
            self._box_height = args[0]
            self._box_width = args[1]
        else:
            raise ValueError
        self._side_length = self._box_height * self._box_width
        
        # Constants
        self._double_loop = [(i, j)
                             for i in range(self._side_length)
                             for j in range(self._side_length)]
        
        # Main data structure
        self._board = np.array(
            [[[True]
              * self._side_length] * self._side_length] * self._side_length,
            dtype=bool)
        
        # __repr__
        if 37 <= self._side_length:
            raise ValueError
        base36digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self._alphabet = base36digits[1:self._side_length+1]

        # Accessible attributes
        self.empties = self._side_length ** 2
        self.depth = -1
        
    def __repr__(self):
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

    def _add(self, digit, row, col):
        """
        Make digit the only candidate in the given square, if possible.
        
        To be used as the only direct interface that modifies this class object.
        
        Returns
        -------
        success : bool
            Whether digit is already a candidate at the given position.
        """

        # Check if digit is actually a candidate in the given square
        if not self._board[digit, row, col]:
            print(self)
            print(digit, row, col)
            raise ValueError(
                f'{digit+1} is not a candidate at ({row+1},{col+1})')

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
        self.empties -= 1
        
        return True
    
    def from_str(self, lst):
        """
        Build the board from the given string or list representation.
        Digits in lst are 1-based, and '.' & '0' represent blank squares.
        """
        self.__init__(self._box_height, self._box_width)
        i = 0
        
        for row, col in self._double_loop:
            digit = lst[i]
            if digit in self._alphabet:
                digit = int(digit, base=36) - 1
                success = self._add(digit, row, col)
                if not success:
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
        operations = OperationQueue(self._side_length)
        while not operations.empty() and niter < 400:
            niter += 1
            operation = operations.get_head()
            i, j = operation.indices

            if operation.finds == 'dig':
                # Find squares with unique digits
                row, col = i, j
                candidates = self._board[:, row, col].nonzero()[0]
                if len(candidates) == 1:
                    digit = candidates[0]
                    if not self._add(digit, row, col):
                        return False
                    # Remove operations referring to this (dig,row,col)
                    # triple and rearrange the remaining ones
                    operations.remove_rearrange(digit, row, col,
                                                self._box_height,
                                                self._box_width)
                else:
                    operations.requeue()

            elif operation.finds == 'row':
                # Find col & digit that has unique row
                digit, col = i, j
                rows = self._board[digit, :, col].nonzero()[0]
                if len(rows) == 1:
                    row = rows[0]
                    if not self._add(digit, row, col):
                        return False
                    operations.remove_rearrange(digit, row, col,
                                                self._box_height,
                                                self._box_width)
                else:
                    operations.requeue()

            elif operation.finds == 'col':
                # Find row & digit that has unique column
                digit, row = i, j
                cols = self._board[digit, row, :].nonzero()[0]
                if len(cols) == 1:
                    col = cols[0]
                    if not self._add(digit, row, col):
                        return False
                    operations.remove_rearrange(digit, row, col,
                                                self._box_height,
                                                self._box_width)
                else:
                    operations.requeue()

            elif operation.finds == 'pos':
                # Find box & digit that has unique position within box
                digit, box = i, j
                row_slice, col_slice = \
                    rows_cols(box, self._box_height, self._box_width)
                positions = \
                    self._board[digit, row_slice, col_slice].nonzero()[0]

                if len(positions) == 1:
                    position = positions[0]
                    row, col = square(box, position,
                                      self._box_height, self._box_width)
                    if not self._add(digit, row, col):
                        return False
                    operations.remove_rearrange(digit, row, col,
                                                self._box_height,
                                                self._box_width)
                else:
                    operations.requeue()

        return True

    def _hidden_clash(self):
        """
        Return None if all squares have at least one possible candidate,
        otherwise return the position of the first found.
        """
        
        for i, j in self._double_loop:
            if len(self._board[:, i, j].nonzero()[0]) == 0:
                return i, j
        
        return None
        
    def _first_empty_square(self):
        """
        Find an empty square to be filled in and return its coordinates.
        """
        
        for row, col in self._double_loop:
            if len(self._board[:, row, col].nonzero()[0]) > 1:
                return row, col
        
        return None, None
    
    def solve(self):
        """
        Solve the board recursively.
        
        Find an empty square, try all possible candidates, and solve each new
        board recursively until first solution found.
        
        Returns
        -------
        sucess : bool
            True if solution found, False when clash occurs.
        """
        
        # Fill in obvious squares in place before recursion
        if not self.quick_fill():
            return False
        
        # Check if finished, FIXME
        
        # Check if there are no-candidate squares
        tpl = self._hidden_clash()
        if tpl is not None:
            return False
        
        # Find a square not yet filled
        i, j = self._first_empty_square()
        if i is None and j is None:
            self.depth = -1
            return True
        
        # Put most probable candidate first, FIXME 30 Mar
        candidates = sorted(self._board[:, i, j].nonzero()[0])
        
        # Recursively call solve() with one new entry
        for digit in candidates:
            child = deepcopy(self)
            child._add(digit, i, j)  # Supposed to always return True
            success = child.solve()
            
            if not success:
                continue
            else:
                if not self._update(child):
                    return False
                self.depth = child.depth + 1
                del child
                return True
        else:
            del child
            return False
    
    def _update(self, obj):
        """
        Update nonzero squares from the board attribute of obj.
        """
        
        for i, j in self._double_loop:
            candidates = obj._board[:, i, j].nonzero()[0]
            if len(candidates) == 1:
                digit = candidates[0]
                success = self._add(digit, i, j)
                if not success:
                    return False
        return True
