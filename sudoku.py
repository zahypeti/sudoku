from __future__ import unicode_literals
from math import sqrt
import string

from solver import Solver


class Sudoku:
    """
    Object that holds the state of a (valid or invalid) sudoku board of a
    fixed size.
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

        # Nested list of ints containing the 1-based digits (or 0 if empty)
        self.board = [
            [0 for _ in range(self._side_length)]
            for _ in range(self._side_length)]

        # Number of empty squares at any point in time
        self.empties = self._side_length ** 2

    def __str__(self):
        """
        User-friendly, readable string description of this Board instance
        showing the current state of the sudoku board. Uses 1-based indexing
        for the digits and arranges them in a square. Shows dots (.) for the
        empty squares.
        """
        result = ''
        for row in self.board:
            for digit in row:
                if 0 < digit:
                    result += str(digit)
                else:
                    result += '.'
            result += '\n'

        return result

    def __repr__(self):
        """
        A short representation of this Board instance showing its size only.

        Use this to create an instance with the initial (empty) state of a
        sudoku board that has the same size as this.
        """
        if self._box_height == self._box_width:
            return '{}({})'.format(self.__class__.__name__, self._side_length)
        else:
            return '{}({}, {})'.format(
                self.__class__.__name__, self._box_height, self._box_width)

    def from_str(self, characters):
        """
        Clear the board and rebuild it from the given character representation.

        Parameters
        ----------
        characters : iterable of length-1 strings
            Single iterable containing the digits (in row-major order) to fill
            the board with. Digits are interpreted using 1-based indexing,
            dot (.) and zero (0) represent empty squares. Characters not in
            _alphabet (or not equal to '0') are ignored.

        Raises
        ------
        ValueError
            If the given character representation does not correspond to a
            valid sudoku board.

        Examples
        --------
        >>> board = Sudoku(4)
        >>> board.from_str('1234....4321....')
        """

        # Clear all squares but keep the current size and shape
        self.__init__(self._box_height, self._box_width)

        # Process characters in parallel with iterating over the squares
        i = 0
        char = characters[i]
        for row in range(self._side_length):
            for col in range(self._side_length):

                char = characters[i]
                # Increase the current position within the input argument
                i += 1

                # Ignore invalid characters
                while char not in (self._alphabet + '0'):
                    char = characters[i]
                    i += 1

                # Dot (.) has the same meaning as zero (0)
                if char == '.':
                    char = '0'

                # Use 1-based indexing internally (and 0 for empty squares)
                self.board[row][col] = int(char, base=36)

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
