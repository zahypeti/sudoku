import unittest

import numpy as np

from board import Board


class TestBoardInit(unittest.TestCase):

    def test_default_board_instantiation(self):
        Board()
        # No errors

    def test_4x4_board_instantiation(self):
        Board(4)
        # No errors

    def test_invalid_side_length(self):
        with self.assertRaises(ValueError):
            Board(8)

    def test_rectangular_board_instantiation(self):
        Board(2, 3)
        # No errors

    def test_too_many_init_arguments(self):
        with self.assertRaises(ValueError):
            Board(3, 3, 9)

    def test_board_too_large(self):
        with self.assertRaises(ValueError):
            Board(37)


class TestFromStr(unittest.TestCase):

    def test_board_from_str_with_obvious_clash(self):
        # Given
        board = Board(4)
        s = '1...1...........'

        # When
        result = board.from_str(s)

        # Then
        self.assertFalse(result)

    def test_valid_board_from_str(self):
        # Given
        board = Board(4)
        s = '1234............'

        # When
        result = board.from_str(s)

        # Then
        self.assertTrue(result)

    def test_board_from_str_with_dots_and_zeros(self):
        # Given
        board = Board(4)
        s = '....0000....1243'

        # When
        result = board.from_str(s)

        # Then
        self.assertTrue(result)


class TestQuickFill(unittest.TestCase):
    def test_quickfill_full(self):
        # Given
        board = Board(4)
        s = '4321123434122143'

        # When
        result = board.quick_fill()

        # Then
        self.assertTrue(result)

    def test_quickfill_empty(self):
        # Given
        empty = Board(4)
        board = Board(4)
        s = '....0000....0000'

        # When
        result = board.quick_fill()

        # Then
        self.assertTrue(result)
        self.assertTrue(np.array_equal(empty._board, board._board))

    def test_quickfill_one_square(self):
        # Given
        board = Board(4)
        s = '12344...0000....'
        expected_str = '1234\n43..\n....\n....\n'

        # When
        board.from_str(s)
        result = board.quick_fill()

        # Then
        self.assertTrue(result)
        self.assertEqual(expected_str, board.__str__())

    def test_quickfill_multiple_solutions(self):
        # Given
        board = Board(4)
        s = '12344..1.......2'  # two different solutions
        # 1234  1234
        # 4..1  4321
        # ....  2  3
        # ...2  3  2

        # When
        board.from_str(s)
        result = board.quick_fill()

        # Then
        self.assertTrue(result)


class TestSolve(unittest.TestCase):
    def test_filled_board(self):
        # Given
        board = Board(4)
        s = '1234432121433412'

        # When
        from_str_success = board.from_str(s)
        success = board.solve()

        # Then
        self.assertTrue(from_str_success)
        self.assertTrue(success)

    def test_board_almost_filled(self):
        # Given
        board = Board(4)
        s = '12344321...33412'

        # When
        board.from_str(s)
        result = board.solve()

        # Then
        self.assertTrue(result)

    def test_empty_3x3_board(self):
        # Given
        board = Board()

        # When
        success = board.solve()

        # Then
        print(board)
        self.assertTrue(success)
