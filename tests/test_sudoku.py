import unittest

from sudoku import Sudoku


class TestSudokuInstantiation(unittest.TestCase):

    def test_default_board_instantiation(self):
        Sudoku()
        # No errors

    def test_4x4_board_instantiation(self):
        Sudoku(4)
        # No errors

    def test_invalid_side_length(self):
        with self.assertRaises(ValueError):
            Sudoku(8)

    def test_rectangular_board_instantiation(self):
        Sudoku(2, 3)
        # No errors

    def test_too_many_init_arguments(self):
        with self.assertRaises(ValueError):
            Sudoku(3, 3, 9)

    def test_init_side_length(self):
        board_6x6 = Sudoku(2, 3)
        self.assertEqual(6, board_6x6._side_length)

    def test_init_alphabet(self):
        expected = '.123456789ABCDEFG'
        board_16x16 = Sudoku(16)
        self.assertEqual(expected, board_16x16._alphabet)

    def test_board_too_large(self):
        with self.assertRaises(ValueError):
            Sudoku(37)
