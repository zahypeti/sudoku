from math import sqrt
import string

from solver import Solver


class Sudoku:
    """

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

        Raises
        ------
        ValueError
            If more than two arguments are provided.
            If the side length is not a square number.
            If the board is too big (side length larger than 36).
        """

        # Parse arguments #####################################################
        if len(args) == 0:
            # Default is a 9x9 board
            self._box_height = 3
            self._box_width = 3

        elif len(args) == 1:
            # Assume a square shaped board with the given side length
            side_length = args[0]
            # Raise error if it's not a square number
            if side_length != int(sqrt(side_length))**2:
                msg = 'The side length of the board must be a square number.'
                raise ValueError(msg)

            # Set the box height and width
            self._box_height = int(sqrt(side_length))
            self._box_width = int(sqrt(side_length))

        elif len(args) == 2:
            self._box_height = args[0]
            self._box_width = args[1]

        else:
            raise ValueError('Too many arguments.')

        # Constant attributes #################################################

        # The side length of the sudoku board
        self._side_length = self._box_height * self._box_width
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
