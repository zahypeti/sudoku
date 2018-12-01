import unittest

import numpy as np

from hb6d_board import HB6DBoard


class TestHB6DBoard(unittest.TestCase):

    def test_init(self):
        HB6DBoard()
        # No errors

    def test_num_row_col_to_idx(self):
        board = HB6DBoard()
        # Zero-based values
        _num = 2
        _row = 3
        _col = 7
        expected_idx = (0, 2, 1, 0, 2, 1)

        _idx = board._num_row_col_to_idx(_num, _row, _col)

        self.assertEqual(_idx, expected_idx)

    def test_idx_to_num_row_col(self):
        board = HB6DBoard()
        _idx = (2, 2, 0, 1, 2, 0)
        expected_num_row_col = (8, 1, 6)

        _num, _row, _col = board._idx_to_num_row_col(_idx)

        self.assertEqual((_num, _row, _col), expected_num_row_col)

    def test_repr(self):
        board = HB6DBoard()
        expected_repr = (
            "1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "\n"
            "1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "\n"
            "1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
        )

        self.assertEqual(repr(board), expected_repr)

    def test_put(self):
        board = HB6DBoard()

        # Insert number 2 into square (3, 1): _num=1, _row=2, _col=0
        board._put((0, 1, 0, 2, 0, 0))

        # No errors

    def test_putting_twice_is_ok(self):
        board = HB6DBoard()
        # Insert number 2 into square (3, 1)
        board._put((0, 1, 0, 2, 0, 0))

        # Do the same insertion again
        board._put((0, 1, 0, 2, 0, 0))

        # No errors

    def test_put_raises(self):
        board = HB6DBoard()
        # Insert number 2 into square (3, 1)
        board._put((0, 1, 0, 2, 0, 0))

        with self.assertRaises(ValueError):
            # Insert a different number (9) into the same square
            board._put((2, 2, 0, 2, 0, 0))

    def test_instantiation_from_array(self):
        squares = np.array([
            [7,    None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
        ])
        expected_str = (
            "7 . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            "---------------------\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            "---------------------\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
        )

        board = HB6DBoard.from_array(squares)

        self.assertEqual(str(board), expected_str)

    def test_candidates(self):
        board = HB6DBoard()

        candidates = board.candidates(6, 2)

        self.assertEqual(candidates, list(range(1, 10)))

    def test_str(self):
        board = HB6DBoard()
        expected_str = (
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            "---------------------\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            "---------------------\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
        )

        self.assertEqual(str(board), expected_str)
