import code
from copy import deepcopy
import numpy as np


DOUBLE_LOOP = [(i,j) for i in range(4) for j in range(4)]


class Board:
    box_shape = (2, 2)
    side_length = 4
    # board is ndarray(4,4,4)
    
    def __init__(self):
        self.board = np.array([[[True] * 4] * 4] * 4, dtype=bool)
        
    def __repr__(self):
        result = ''
        for row in range(4):
            for col in range(4):
                digit = '.'
                candidates = self.board[:, row, col].nonzero()[0]
                if len(candidates) == 1:
                    digit = str(1 + candidates[0])
                result += digit
            result += '\n'
        return result
        # or try list comprehension
        # ['.' if only_one else whatev for col in range(4) for row in range(4)]
    
    def add(self, candidate, row, col):
        """
        Make candidate the only one in the given cell if possible.
        
        Returns
        -------
        success : bool
            Whether candidate is already a candidate at the given position.
        """
        # Check if actually a candidate in the given cell
        if not self.board[candidate, row, col]:
            return False
        
        # Remove same candidates in row, col
        self.board[candidate, :, col] = [False] * 4
        self.board[candidate, row, :] = [False] * 4
        
        # Remove same candidates in box, FIXME 30 Mar 2018
        
        # Remove other candidates in cell
        self.board[:, row, col] = [False] * 4
        
        # Make this a candidate in the cell
        self.board[candidate, row, col] = True
        
        return True
    
    def from_str(self, lst):
        """
        Build the board from the given string or list representation.
        Candidates are 1-based, '.' and '0' represent missing values.
        """
        self.__init__()
        i = 0
        
        for row in range(4):
            for col in range(4):
            
                candidate = lst[i]
                if candidate in '1234':
                    candidate = int(candidate)-1
                    success = self.add(candidate, row, col)
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
            for i, j in DOUBLE_LOOP:
                
                # Find cells with unique candidates
                row, col = i, j
                candidates = self.board[:, row, col].nonzero()[0]
                if len(candidates) == 1:
                    candidate = candidates[0]
                    if not self.add(candidate, row, col):
                        return False
        
                # Find row & candidate that has unique column
                row, candidate = i, j
                cols = self.board[candidate, row, :].nonzero()[0]
                if len(cols) == 1:
                    col = cols[0]
                    if not self.add(candidate, row, col):
                        return False
                
                # Find col & candidate that has unique row
                col, candidate = i, j
                rows = self.board[candidate, :, col].nonzero()[0]
                if len(rows) == 1:
                    row = rows[0]
                    if not self.add(candidate, row, col):
                        return False
                
                # Find box & candidate that has unique position within box
                # FIXME 30 Mar 2018
                box, candidate = i, j 
                positions = []  # .nonzero()[0] FIXME
                if len(positions) == 1:
                    position = positions(0)
                    # row, col = ...
                    # OR: use self.add with alternative indexing
                    if not self.add(candidate, row, col):
                        return False
                
        return True
    
    def _hidden_clash(self):
        """
        Return None if all cells have at least one possible candidate, otherwise return the position of the first found.
        """
        
        for i,j in DOUBLE_LOOP:
            if len(self.board[:,i,j].nonzero()[0]) == 0:
                return i,j
        
        return None
        
    
    def _first_empty_cell(self):
        """
        Find an empty cell to be filled in and return its coordinates.
        """
        
        for row, col in DOUBLE_LOOP:
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
            child.add(candidate, i, j)  # Supposed to always return True
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
        
        for i,j in DOUBLE_LOOP:
            candidates = obj.board[:, i, j].nonzero()[0]
            if len(candidates) == 1:
                candidate = candidates[0]
                success = self.add(candidate, i, j)
                if not success:
                    return False
        return True
