import unittest


class TestReadmeExample(unittest.TestCase):

    def test_readme_example(self):
        """
        This test is covering the example script in `README.md`.
        Make sure it is up to date.
        """
        # Given
        squares = [
            [4, 0, 0, 0, 0, 0, 8, 0, 5],
            [0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 7, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 6, 0],
            [0, 0, 0, 0, 8, 0, 4, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 3, 0, 7, 0],
            [5, 0, 0, 2, 0, 0, 0, 0, 0],
            [1, 0, 4, 0, 0, 0, 0, 0, 0],
        ]

        # When
        from sudoku.api import Board
        my_board = Board.from_array(squares)
        my_board.solve()
        # Use str() instead of print() to keep the test output clean
        str(my_board)

        # Then there's no error
