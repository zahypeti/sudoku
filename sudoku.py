from math import sqrt
import string

from solver import Solver


class Sudoku:
    """

    """
    def __init__(self, side_length):
        # Parse arguments TODO

        # Constant attributes #################################################

        # The side length of the sudoku board
        self._side_length = side_length
        # Raise an error if characters would run out due to a large board size
        if 37 <= self._side_length:
            msg = 'The side length of the board must be less than 37.'
            raise ValueError(msg)

        # Create the string containing all possible digits up to base 36
        base36digits = string.digits + string.ascii_uppercase
        # Characters used for user-friendly square representation: .,1,2,3 etc
        self._alphabet = '.' + base36digits[1:self._side_length+1]


        # Non-constant attributes #############################################

        self.board = [[0] * self._side_length] * self._side_length
        # Number of empty squares at any point in time
        self.empties = self._side_length ** 2

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def from_str(self):
        pass

    def from_file(self):
        pass

    def solve(self):
        # Instatiate the solver object with the current state of the board
        array = func(self.board)
        solver = Solver(array)

        # Try solving the board completely
        try:
            array = solver.recursively_solve()
        except RuntimeError:
            msg = 'Invalid sudoku board, no solution.'
            print(msg)
            return

        # Get user-friendly representation
        self.board = invfunc(array)
