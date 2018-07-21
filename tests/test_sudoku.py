import unittest

from sudoku import Sudoku


class TestSudoku(unittest.TestCase):

    def test_board_too_large(self):
        with self.assertRaises(ValueError):
            Sudoku(37)
