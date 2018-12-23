import unittest

from sudoku.indexing import _boxrows, _boxcols, boxindex, rows_cols, square


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

    def test_boxcols_last(self):
        # Given
        col = 8
        box_width = 3
        expected_result = slice(6,9)

        # When
        result = _boxcols(col, box_width)

        # Then
        self.assertEqual(expected_result, result)

    def test_boxindex(self):
        # Given
        row, col = 0, 2
        box_height, box_width = 3, 3
        expected_box_id = 0

        # When
        box_id = boxindex(row, col, box_height, box_width)

        # Then
        self.assertEqual(expected_box_id, box_id)

    def test_boxindex_rectangular(self):
        # Given
        row, col = 3, 4
        box_height, box_width = 3, 2
        expected_box_id = 5

        # When
        box_id = boxindex(row, col, box_height, box_width)

        # Then
        self.assertEqual(expected_box_id, box_id)

    def test_rows_cols_box_on_diagonal(self):
        # Given
        box = 4
        box_height, box_width = 3, 3
        expected_row_slice = slice(3, 6)
        expected_col_slice = slice(3, 6)

        # When
        row_slice, col_slice = rows_cols(box, box_height, box_width)

        # Then
        self.assertEqual(expected_row_slice, row_slice)
        self.assertEqual(expected_col_slice, col_slice)

    def test_rows_cols_box(self):
        # Given
        box = 6
        box_height, box_width = 3, 3
        expected_row_slice = slice(6, 9)
        expected_col_slice = slice(0, 3)

        # When
        row_slice, col_slice = rows_cols(box, box_height, box_width)

        # Then
        self.assertEqual(expected_row_slice, row_slice)
        self.assertEqual(expected_col_slice, col_slice)

    def test_rows_cols_diagonal_square(self):
        # Given
        row, col = 3, 3
        box_height, box_width = 3, 3
        expected_row_slice = slice(3, 6)
        expected_col_slice = slice(3, 6)

        # When
        row_slice, col_slice = rows_cols(row, col, box_height, box_width)

        # Then
        self.assertEqual(expected_row_slice, row_slice)
        self.assertEqual(expected_col_slice, col_slice)

    def test_rows_cols_square(self):
        # Given
        row, col = 2, 7
        box_height, box_width = 3, 3
        expected_row_slice = slice(0, 3)
        expected_col_slice = slice(6, 9)

        # When
        row_slice, col_slice = rows_cols(row, col, box_height, box_width)

        # Then
        self.assertEqual(expected_row_slice, row_slice)
        self.assertEqual(expected_col_slice, col_slice)

    def test_square(self):
        # Given
        box_height, box_width = 3, 3
        box, pos = 0, 3
        expected_row, expected_col = 1, 0

        # When
        row, col = square(box, pos, box_height, box_width)

        # Then
        self.assertEqual(expected_row, row)
        self.assertEqual(expected_col, col)

    def test_square_rectangular(self):
        # Given
        box_height, box_width = 1, 3
        box, pos = 2, 2
        expected_row, expected_col = 2, 2

        # When
        row, col = square(box, pos, box_height, box_width)

        # Then
        self.assertEqual(expected_row, row)
        self.assertEqual(expected_col, col)
