from copy import deepcopy
from math import sqrt
import numpy as np


class Board:

    def __init__(self, *args):
        if len(args) == 0:
            self.box_height = 3
            self.box_width = 3
            self.side_length = self.box_height * self.box_width
        elif len(args) == 1:
            self.side_length = args[0]
            # Assume square box, FIXME 31 Mar 2018
            self.box_height = int(sqrt(self.side_length))
            self.box_width = int(sqrt(self.side_length))
        elif len(args) == 2:
            self.box_height = args[0]
            self.box_width = args[1]
            self.side_length = self.box_height * self.box_width
        else:
            raise ValueError
        
        if 37 <= self.side_length:
            raise ValueError
        base36digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.alphabet = base36digits[1:self.side_length+1]
        
        self.double_loop = [(i,j) for i in range(self.side_length) for j in range(self.side_length)]
        
        self.board = np.array([[[True] * self.side_length] * self.side_length] * self.side_length, dtype=bool)
        
        self._row_col_quickfilled = np.array([[False] * self.side_length] * self.side_length)
        self._dig_row_quickfilled = np.array([[False] * self.side_length] * self.side_length)
        self._dig_col_quickfilled = np.array([[False] * self.side_length] * self.side_length)
        self._dig_box_quickfilled = np.array([[False] * self.side_length] * self.side_length)
        
        self.empties = self.side_length ** 2
        
    def __repr__(self):
        result = ''
        for row, col in self.double_loop:
            candidates = self.board[:, row, col].nonzero()[0]
            if len(candidates) == 1:
                result += self.alphabet[candidates[0]]
            else:
                result += '.'
            if col == self.side_length - 1:
                result += '\n'
        return result
    
    def _boxrows(self, row):
        """
        Return a tuple (start,end) used for array slicing, that corresponds to the rows of the box containing the given single row.
        """
        start = row // self.box_height * self.box_height
        finish = start + self.box_height
        return (start, finish)
        
        return [(r//self.box_height == row//self.box_height) for r in range(self.side_length)]
    
    def _boxcols(self, col):
        """
        Return a tuple (start,end) used for array slicing, that corresponds to the columns of the box containing the given single column.
        """
        start = col // self.box_width * self.box_width
        finish = start + self.box_width
        return (start, finish)
    
    def _boxindex(self, row, col):
        """
        Return the index of the box containing the given cell.
        """
        return row//self.box_height*self.box_height + col%self.box_width
    
    def _add(self, digit, row, col):
        """
        Make digit the only candidate in the given cell, if possible.
        
        Use this as the only single interface to modify `self.board`.
        
        Returns
        -------
        success : bool
            Whether digit is already a candidate at the given position.
        """
        # Check if digit is actually a candidate in the given cell
        if not self.board[digit, row, col]:
            return False
        
        # Calculate box_rows, box_cols, box
        srow, erow = self._boxrows(row)
        scol, ecol = self._boxcols(col)
        box = self._boxindex(row, col)
        
        # Remove other digits in cell, and same digits in row & col
        self.board[:, row, col] = [False] * self.side_length
        self.board[digit, row, :] = [False] * self.side_length
        self.board[digit, :, col] = [False] * self.side_length
        
        # Remove same digits in box
        self.board[digit:digit+1, srow:erow, scol:ecol] = [[False] * self.box_width] * self.box_height  # slice
        
        # Make this a digit in the cell
        self.board[digit, row, col] = True
        
        # Update quick_fill'ed cells
        self._row_col_quickfilled[row, col] = True
        self._dig_row_quickfilled[digit, row] = True
        self._dig_col_quickfilled[digit, col] = True
        self._dig_box_quickfilled[digit, box] = True
        
        # Update attributes
        self.empties -= 1
        
        return True
    
    def from_str(self, lst):
        """
        Build the board from the given string or list representation.
        Candidates are 1-based, '.' and '0' represent missing values.
        """
        self.__init__(self.side_length)
        i = 0
        
        for row, col in self.double_loop:
            candidate = lst[i]
            if candidate in [str(x) for x in range(1,self.side_length+1)]:
                candidate = int(candidate)-1
                success = self._add(candidate, row, col)
                if not success:
                    self.__init__()
                    return False
            i += 1
                
        return True
        
    def quick_fill(self):
        """
        Fill in the obvious candidates in place.
        
        Returns
        -------
        success : bool
            False if detects immediate clash during the process, True otherwise.
        """
        
        # repeat this until no new entry, FIXME 30 Mar 2018
        for _ in range(10):
            # for i, j in itertools.product(range(4), range(4)):
            for i, j in self.double_loop:
                
                # Find cells with unique candidates
                row, col = i, j
                if not self._row_col_quickfilled[row, col]:
                    candidates = self.board[:, row, col].nonzero()[0]
                    if len(candidates) == 1:
                        digit = candidates[0]
                        if not self._add(digit, row, col):
                            return False
        
                # Find row & digit that has unique column
                digit, row = i, j
                if not self._dig_row_quickfilled[digit, row]:
                    cols = self.board[digit, row, :].nonzero()[0]
                    if len(cols) == 1:
                        col = cols[0]
                        if not self._add(digit, row, col):
                            return False
                
                # Find col & digit that has unique row
                digit, col = i, j
                if not self._dig_col_quickfilled[digit, col]:
                    rows = self.board[digit, :, col].nonzero()[0]
                    if len(rows) == 1:
                        row = rows[0]
                        if not self._add(digit, row, col):
                            return False
                
                # Find box & digit that has unique position within box
                # FIXME 30 Mar 2018
                digit, box = i, j
                if not self._dig_box_quickfilled[digit, box]:
                    positions = []  # .nonzero()[0] FIXME
                    if len(positions) == 1:
                        position = positions(0)
                        # row, col = ...
                        # OR: use self.add with alternative indexing
                        if not self._add(digit, row, col):
                            return False
                
        return True
    
    def _hidden_clash(self):
        """
        Return None if all cells have at least one possible candidate, otherwise return the position of the first found.
        """
        
        for i,j in self.double_loop:
            if len(self.board[:,i,j].nonzero()[0]) == 0:
                return i,j
        
        return None
        
    def _first_empty_cell(self):
        """
        Find an empty cell to be filled in and return its coordinates.
        """
        
        for row, col in self.double_loop:
            if len(self.board[:, row, col].nonzero()[0]) > 1:
                return row, col
        
        return None, None
    
    def solve(self):
        """
        Solve the board recursively.
        
        Find an empty cell, try all possible candidates, and solve each new board until first solution found.
        
        Returns
        -------
        sucess : bool
            True if solution found, False when clash occurs.
        """
        
        # Fill in obvious cells in place before recursion
        if not self.quick_fill():
            return False
        
        # Check if finished, FIXME
        
        # Check if there are no-candidate cells
        tpl = self._hidden_clash()
        if tpl is not None:
            return False
        
        # Find a cell not yet filled
        i,j = self._first_empty_cell()
        if i is None and j is None:
            return True
        
        # Put most probable candidate first, FIXME 30 Mar
        candidates = sorted(self.board[:, i, j].nonzero()[0])
        
        # Recursively call solve() with one new entry
        for candidate in candidates:
            child = deepcopy(self)
            child._add(candidate, i, j)  # Supposed to always return True
            success = child.solve()
            
            if not success:
                continue
            else:
                if not self.update(child):
                    return False
                del child
                return True
        else:
            del child
            return False
    
    def update(self, obj):
        """
        Update nonzero cells from the board attribute of obj.
        """
        
        for i,j in self.double_loop:
            candidates = obj.board[:, i, j].nonzero()[0]
            if len(candidates) == 1:
                candidate = candidates[0]
                success = self._add(candidate, i, j)
                if not success:
                    return False
        return True
