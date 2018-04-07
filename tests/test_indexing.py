import unittest

from indexing import _boxrows, _boxcols


class TestIndexing(unittest.TestCase):

    def test_boxrows_zeroth(self):
        # Given
        row = 0
        box_height = 5
        expected_result = slice(0,5)

        # When
        result = _boxrows(row, box_height)

        # Then
        self.assertEqual(expected_result, result)

    def test_boxrows(self):
        # Given
        row = 6
        box_height = 3
        expected_result = slice(6,9)

        # When
        result = _boxrows(row, box_height)

        # Then
        self.assertEqual(expected_result, result)

    def test_boxcols(self):
        # Given
        col = 4
        box_width = 3
        expected_result = slice(3,6)

        # When
        result = _boxcols(col, box_width)

        # Then
        self.assertEqual(expected_result, result)
