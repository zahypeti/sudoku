import unittest

from ..board import Board

class TestBoard(unittest.TestCase):
    def test_board_obvious_clash(self):
        # Given
        board = Board(4)
        s = '1...1...........'

        # When
        result = board.from_str(s)
        
        # Then
        self.assertFalse(result)
