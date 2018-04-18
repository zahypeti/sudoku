import unittest

from board import Board


class TestBoard(unittest.TestCase):

    def test_board_from_str_obvious_clash(self):
        # Given
        board = Board(4)
        s = '1...1...........'

        # When
        result = board.from_str(s)

        # Then
        self.assertFalse(result)

    def test_board_from_str_valid_board(self):
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


    def test_filled_board(self):
        # Given
        board = Board(4)
        s = '1234432121433412'

        # When
        board.from_str(s)
        result = board.solve()

        # Then
        print(board)
        self.assertTrue(result)

    def test_board_almost_filled(self):
        # Given
        board = Board(4)
        s = '12344321...33412'

        # When
        board.from_str(s)
        result = board.solve()

        # Then
        print(board)
        self.assertTrue(result)

    def test_board(self):
        # Given
        board = Board(4)
        s = '12344..1.......2'

        # When
        board.from_str(s)
        result = board.solve()

        # Then
        print(board)
        self.assertTrue(result)
