import unittest

from sudoku import Sudoku


class TestSudokuInstantiation(unittest.TestCase):

    def test_default_Sudoku_instantiation(self):
        Sudoku()
        # No errors

    def test_Sudoku_too_large(self):
        with self.assertRaises(ValueError):
            Sudoku(37)

    def test_4x4_Sudoku_instantiation(self):
        Sudoku(4)
        # No errors

    def test_invalid_side_length(self):
        with self.assertRaises(ValueError):
            Sudoku(8)

    def test_rectangular_Sudoku_instantiation(self):
        Sudoku(2, 3)
        # No errors

    def test_too_many_init_arguments(self):
        with self.assertRaises(ValueError):
            Sudoku(3, 3, 9)

    def test_init_side_length(self):
        Sudoku_6x6 = Sudoku(2, 3)
        self.assertEqual(6, Sudoku_6x6._side_length)

    def test_init_alphabet(self):
        expected = '.123456789ABCDEFG'
        Sudoku_16x16 = Sudoku(16)
        self.assertEqual(expected, Sudoku_16x16._alphabet)

    def test_init_Sudoku(self):
        sudoku = Sudoku(3, 4)
        self.assertEqual(sudoku.board, [[0] * 12] * 12)

    def test_init_empties(self):
        sudoku = Sudoku(16)
        self.assertEqual(sudoku.empties, 256)


class TestSudokuStr(unittest.TestCase):

    def test_empty_Sudoku_str(self):
        expected = (
            '....\n'
            '....\n'
            '....\n'
            '....\n')
        Sudoku_4x4 = Sudoku(4)
        self.assertEqual(expected, str(Sudoku_4x4))

    def test_nonempty_Sudoku_str(self):
        sudoku = Sudoku(2, 2)
        sudoku.board = [[1, 2, 0, 0], [3, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(str(sudoku), '12..\n34..\n....\n....\n')


class TestSudokuRepr(unittest.TestCase):

    def test_Sudoku_repr_of_9x9(self):
        expected = 'Sudoku(9)'
        sudoku_9x9 = Sudoku(9)
        self.assertEqual(expected, repr(sudoku_9x9))

    def test_Sudoku_repr_of_12x12(self):
        expected = 'Sudoku(3, 4)'
        sudoku_3x4 = Sudoku(3, 4)
        self.assertEqual(expected, repr(sudoku_3x4))


class TestFromStr(unittest.TestCase):

    def test_valid_Sudoku_from_str(self):
        # Given
        sudoku = Sudoku(4)
        s = '1234............'

        # When
        sudoku.from_str(s)

        # Then
        self.assertEqual(sudoku.board, [[1, 2, 3, 4], [0]*4, [0]*4, [0]*4])

    def test_Sudoku_from_str_with_dots_and_zeros(self):
        # Given
        sudoku = Sudoku(4)
        s = '....0000....1243'

        # When
        sudoku.from_str(s)

        # Then
        self.assertEqual(sudoku.board, [[0]*4, [0]*4, [0]*4, [1, 2, 4, 3]])

    def test_ignore_unknown_characters_from_str(self):
        string = (
            '12|34\n'
            '..|..\n'
            '-----\n'
            '..|..\n'
            '..|..\n')
        sudoku_4x4 = Sudoku(4)
        sudoku_4x4.from_str(string)
        self.assertEqual(sudoku_4x4.board, [[1, 2, 3, 4], [0]*4, [0]*4, [0]*4])


class TestFromTxtFile(unittest.TestCase):

    def test_from_txt_file(self):
        fname = 'tests/examples/rectangular_2x3/example1.txt'
        board = Sudoku(2, 3)
        board.from_txt_file(fname)


class TestSolveSudoku():
    pass
