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

    def test_init_side_length(self):
        board_6x6 = Board(2, 3)
        self.assertEqual(6, board_6x6._side_length)

    def test_init_double_loop(self):
        expected = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)]
        board_3x3 = Board(1, 3)
        self.assertEqual(expected, board_3x3._double_loop)

    def test_init_alphabet(self):
        expected = '.123456789ABCDEFG'
        board_16x16 = Board(16)
        self.assertEqual(expected, board_16x16._alphabet)


class TestBoardStr(unittest.TestCase):

    def test_empty_board_str(self):
        expected = (
            '....\n'
            '....\n'
            '....\n'
            '....\n')
        board_4x4 = Board(4)
        self.assertEqual(expected, str(board_4x4))

    def test_nonempty_board_str(self):
        expected = (
            '1234\n'
            '3412\n'
            '4321\n'
            '2143\n')
        board4x4 = Board(4)
        board4x4.from_str('123434124321....')
        self.assertEqual(expected, str(board4x4))


class TestBoardRepr(unittest.TestCase):

    def test_board_repr_of_9x9(self):
        expected = 'Board(9)'
        board_9x9 = Board(9)
        self.assertEqual(expected, repr(board_9x9))

    def test_board_repr_of_12x12(self):
        expected = 'Board(3, 4)'
        board_3x4 = Board(3, 4)
        self.assertEqual(expected, repr(board_3x4))


class TestFromStr(unittest.TestCase):

    def test_board_from_str_with_obvious_clash(self):
        # Given
        board = Board(4)
        s = '1...1...........'

        with self.assertRaises(ValueError):
            board.from_str(s)

    def test_valid_board_from_str(self):
        # Given
        board = Board(4)
        s = '1234............'

        # When
        board.from_str(s)

        # Then
        self.assertEqual('1234\n....\n....\n....\n', str(board))

    def test_board_from_str_with_dots_and_zeros(self):
        # Given
        board = Board(4)
        s = '....0000....1243'

        # When
        board.from_str(s)

        # Then
        self.assertEqual('....\n....\n....\n1243\n', str(board))

    def test_ignore_unknown_characters_from_str(self):
        string = (
            '12|34\n'
            '..|..\n'
            '-----\n'
            '..|..\n'
            '..|..\n')
        board_4x4 = Board(4)
        board_4x4.from_str(string)
        self.assertEqual('1234\n....\n....\n....\n', str(board_4x4))


class TestQuickFill(unittest.TestCase):

    def test_quickfill_empty_1x1(self):
        board_1x1 = Board(1)

        result = board_1x1.quick_fill()

        self.assertTrue(result)
        self.assertEqual('1\n', str(board_1x1))

    def test_quickfill_full_1x1(self):
        board_1x1 = Board(1)
        board_1x1.from_str('1')

        result = board_1x1.quick_fill()

        self.assertTrue(result)
        self.assertEqual('1\n', str(board_1x1))

    def test_quickfill_empty_2x2(self):
        board_2x2 = Board(1, 2)
        result = board_2x2.quick_fill()
        self.assertTrue(result)
        self.assertEqual('..\n..\n', str(board_2x2))

    def test_quickfill_half_done_2x2(self):
        board_2x2 = Board(1, 2)
        board_2x2.from_str('1...')

        result = board_2x2.quick_fill()

        self.assertTrue(result)
        self.assertEqual('12\n21\n', str(board_2x2))

    def test_quickfill_full_2x2(self):
        board_2x2 = Board(1, 2)
        board_2x2.from_str('1221')

        result = board_2x2.quick_fill()

        self.assertTrue(result)
        self.assertEqual('12\n21\n', str(board_2x2))

    def test_quickfill_empty_3x3(self):
        board_3x3 = Board(1, 3)
        result = board_3x3.quick_fill()
        self.assertTrue(result)
        self.assertEqual('...\n...\n...\n', str(board_3x3))

    def test_quickfill_almost_empty_3x3(self):
        board_3x3 = Board(1, 3)
        board_3x3.from_str('120...000')

        result = board_3x3.quick_fill()

        self.assertTrue(result)
        self.assertEqual('123\n...\n...\n', str(board_3x3))

    def test_quickfill_halfway_3x3(self):
        board_3x3 = Board(1, 3)
        board_3x3.from_str('1...1...1')

        result = board_3x3.quick_fill()

        self.assertTrue(result)
        self.assertEqual('1..\n.1.\n..1\n', str(board_3x3))

    def test_quickfill_halfway_plus_3x3(self):
        board_3x3 = Board(1, 3)
        board_3x3.from_str('12..1...1')

        result = board_3x3.quick_fill()

        self.assertTrue(result)
        self.assertEqual('123\n312\n231\n', str(board_3x3))

    def test_quickfill_almost_full_3x3(self):
        board_3x3 = Board(1, 3)
        board_3x3.from_str('1202..000')

        result = board_3x3.quick_fill()

        self.assertTrue(result)
        self.assertEqual('123\n231\n312\n', str(board_3x3))

    def test_quickfill_full_3x3(self):
        board_3x3 = Board(1, 3)
        board_3x3.from_str('123231312')

        result = board_3x3.quick_fill()

        self.assertTrue(result)
        self.assertEqual('123\n231\n312\n', str(board_3x3))

    def test_quickfill_full_4x4(self):
        # Given
        board = Board(4)
        s = '4321123434122143'

        # When
        result = board.quick_fill()

        # Then
        self.assertTrue(result)

    def test_quickfill_empty_4x4(self):
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

    def test_solve_empty_1x1(self):
        board_1x1 = Board(1)
        result = board_1x1.solve()
        self.assertTrue(result)
        self.assertEqual('1\n', str(board_1x1))

    def test_solve_empty_2x2(self):
        board_2x2 = Board(1, 2)
        result = board_2x2.solve()
        self.assertTrue(result)
        # Check that it finds one of the results
        self.assertIn(str(board_2x2), ['12\n21\n', '21\n12\n'])

    def test_solve_empty_3x3(self):
        board_3x3 = Board(1, 3)
        result = board_3x3.solve()
        self.assertTrue(result)
        # Check that it finds the "first" result
        self.assertIn(str(board_3x3), ['123\n231\n312\n'])

    def test_solve_empty_4x4(self):
        board_4x4 = Board(4)
        result = board_4x4.solve()
        self.assertTrue(result)
        # Check that it finds the "first" result
        self.assertIn(str(board_4x4), ['1234\n3412\n2143\n4321\n'])

    def test_filled_board(self):
        # Given
        board = Board(4)
        s = '1234432121433412'

        # When
        board.from_str(s)
        success = board.solve()
        print(success)

        # Then
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
        self.assertTrue(success)

    def test_solve_almost_empty_3x3(self):
        board = Board()
        board._add(0, 0, 0)

        result = board.solve()

        self.assertTrue(result)
