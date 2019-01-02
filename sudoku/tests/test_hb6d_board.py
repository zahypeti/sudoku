import unittest

import numpy as np

from sudoku.hb6d_board import ConsistencyError, HB6DBoard


class TestHB6DBoard(unittest.TestCase):

    def test_init(self):
        HB6DBoard()
        # No errors

    def test_num_row_col_to_idx(self):
        # Convert _num, _row, and _col to 6D coordinates
        board = HB6DBoard()
        # Zero-based values
        _num = 2
        _row = 3
        _col = 7
        expected_idx = (0, 2, 1, 0, 2, 1)

        _idx = board._num_row_col_to_idx(_num, _row, _col)

        self.assertEqual(_idx, expected_idx)

    def test_idx_to_num_row_col(self):
        # Convert 6D coordinates to _num, _row, and _col
        board = HB6DBoard()
        _idx = (2, 2, 0, 1, 2, 0)
        expected_num_row_col = (8, 1, 6)

        _num, _row, _col = board._idx_to_num_row_col(_idx)

        self.assertEqual((_num, _row, _col), expected_num_row_col)


class TestPutMethod(unittest.TestCase):

    def test_simple_put(self):
        board = HB6DBoard()
        expected_repr = (
            "1 . 3 | 1 . 3 | 1 . 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 . 3 | 1 . 3 | 1 . 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            ". 2 . | 1 . 3 | 1 . 3  1 . 3 | 1 . 3 | 1 . 3  1 . 3 | 1 . 3 | 1 . 3\n"  # noqa: E501
            ". . . | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            ". . . | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "\n"
            "1 . 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 . 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 . 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "\n"
            "1 . 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 . 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 . 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9\n"  # noqa: E501
        )

        # Insert number 2 into square (3, 1): _num=1, _row=2, _col=0
        board._put((0, 1, 0, 2, 0, 0))

        # No errors
        self.assertEqual(repr(board), expected_repr)

    def test_put(self):
        board = HB6DBoard()
        expected_repr = (
            "1 . 3 | 1 . 3 | 1 . 3  1 2 3 | 1 . 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | . 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 . 3 | 1 . 3 | 1 . 3  1 2 3 | 1 . 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | . 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            ". 2 . | 1 . 3 | 1 . 3  1 . 3 | 1 . 3 | 1 . 3  1 . 3 | 1 . 3 | 1 . 3\n"  # noqa: E501
            ". . . | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            ". . . | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | . 8 9\n"  # noqa: E501
            "\n"
            "1 . 3 | 1 . 3 | 1 . 3  1 . 3 | . 2 . | 1 . 3  1 . 3 | 1 . 3 | 1 . 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | . . . | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | . . . | 7 8 9  7 8 9 | 7 8 9 | . 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 . 3 | 1 2 3 | 1 2 3  1 . 3 | 1 . 3 | 1 . 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | . 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 . 3 | 1 2 3 | 1 2 3  1 . 3 | 1 . 3 | 1 . 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | . 8 9\n"  # noqa: E501
            "\n"
            "1 . 3 | 1 2 3 | 1 2 3  1 2 3 | 1 . 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  . 8 9 | . 8 9 | . 8 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 . 3 | 1 2 3 | 1 2 3  1 2 3 | 1 . 3 | 1 2 3  1 2 3 | 1 2 3 | . . .\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | . . .\n"  # noqa: E501
            ". 8 9 | . 8 9 | . 8 9  . 8 9 | . 8 9 | . 8 9  . 8 9 | . 8 9 | 7 . .\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 . 3 | 1 2 3 | 1 2 3  1 2 3 | 1 . 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  . 8 9 | . 8 9 | . 8 9\n"  # noqa: E501
        )

        # Insert number 2 into square (3, 1): _num=1, _row=2, _col=0
        board._put((0, 1, 0, 2, 0, 0))
        # Insert number 2 into square (4, 5): _num=1, _row=3, _col=4
        board._put((0, 1, 1, 0, 1, 1))
        # Insert number 7 into square (8, 9): _num=6, _row=7, _col=8
        board._put((2, 0, 2, 1, 2, 2))

        # No errors
        self.assertEqual(repr(board), expected_repr)

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


class TestBoardFromArray(unittest.TestCase):

    def test_instantiation_from_array(self):
        squares = np.array([
            [7,    None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, 7,    None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, 3,    None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, 2,    1,    None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
        ])
        expected_str = (
            "7 . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            "---------------------\n"
            ". . . | . . . | . 7 .\n"
            ". . . | . . . | . . .\n"
            ". 3 . | . . . | . . .\n"
            "---------------------\n"
            ". . . | . . . | 2 1 .\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
        )

        board = HB6DBoard.from_array(squares)

        self.assertEqual(str(board), expected_str)

    def test_instantiation_from_array_raises(self):
        squares = np.array([
            [7,    None, None, None, None, None, None, None, None],  # noqa: E241
            [7,    None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
        ])

        with self.assertRaises(ConsistencyError) as exc_cm:
            board = HB6DBoard.from_array(squares)

        self.assertIn("Clash found", str(exc_cm.exception))


class TestCandidates(unittest.TestCase):

    def test_candidates(self):
        squares = np.array([
            [7,    None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, 7,    None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, 3,    None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, 2,    1,    None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
        ])
        board = HB6DBoard.from_array(squares)
        # 2, 3, and 7 are not candidates, but every other number is
        expected_candidates = [1, 4, 5, 6, 8, 9]

        candidates = board.candidates(6, 7)

        self.assertEqual(candidates, expected_candidates)


class TestInsert(unittest.TestCase):

    def test_insert(self):
        squares = np.array([
            [7,    None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, 7,    None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, 3,    None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, 2,    1,    None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
        ])
        board = HB6DBoard.from_array(squares)
        expected_candidates = [9]

        board.insert(number=9, row=1, column=2)

        self.assertEqual(board.candidates(1, 2), expected_candidates)

    def test_insert_raises(self):
        squares = np.array([
            [7,    None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, 7,    None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, 3,    None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, 2,    1,    None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
        ])
        board = HB6DBoard.from_array(squares)

        with self.assertRaises(ValueError) as exc_cm:
            board.insert(number=2, row=6, column=7)

        self.assertIn("not a valid candidate", str(exc_cm.exception))


class TestQuickFill(unittest.TestCase):

    def test_quick_fill(self):
        squares = np.array([
            [0, 0, 3, 0, 2, 0, 6, 0, 0],
            [9, 0, 0, 3, 0, 5, 0, 0, 1],
            [0, 0, 1, 8, 0, 6, 4, 0, 0],
            [0, 0, 8, 1, 0, 2, 9, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 0, 6, 7, 0, 8, 2, 0, 0],
            [0, 0, 2, 6, 0, 9, 5, 0, 0],
            [8, 0, 0, 2, 0, 3, 0, 0, 9],
            [0, 0, 5, 0, 1, 0, 3, 0, 0],
        ])
        board = HB6DBoard.from_array(squares)
        expected_str = (
            "4 8 3 | 9 2 1 | 6 5 7\n"
            "9 6 7 | 3 4 5 | 8 2 1\n"
            "2 5 1 | 8 7 6 | 4 9 3\n"
            "---------------------\n"
            "5 4 8 | 1 3 2 | 9 7 6\n"
            "7 2 9 | 5 6 4 | 1 3 8\n"
            "1 3 6 | 7 9 8 | 2 4 5\n"
            "---------------------\n"
            "3 7 2 | 6 8 9 | 5 1 4\n"
            "8 1 4 | 2 5 3 | 7 6 9\n"
            "6 9 5 | 4 1 7 | 3 8 2\n"
        )

        board._quick_fill()

        self.assertEqual(str(board), expected_str)

    def test_quick_fill_invalid_board(self):
        # Invalid board with no possible candidate in the top left square
        squares = np.array([
            [0, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
        ])
        board = HB6DBoard.from_array(squares)
        # The obvious squares should be filled in still
        expected_str = (
            ". 2 3 | 4 5 6 | 7 8 9\n"
            "1 . . | . . . | . . .\n"
            ". . . | . . . | 1 . .\n"  # there's a new entry in this row
            "---------------------\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . 1 .\n"
            "---------------------\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . .\n"
            ". . . | . . . | . . 1\n"
        )

        board._quick_fill()

        self.assertEqual(str(board), expected_str)

    def test_quick_fill_twice_is_redundant(self):
        """
        Check that calling `_quick_fill()` a second time doesn't do anything.
        """
        # Given
        squares = np.array([
            [0, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 9, 0, 7],
            [0, 7, 6, 0, 2, 0, 3, 0, 0],
            [0, 0, 0, 0, 7, 0, 0, 3, 0],
            [0, 0, 1, 2, 0, 5, 4, 0, 0],
            [0, 9, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 5, 0, 6, 0, 2, 9, 0],
            [6, 0, 4, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 5, 0],
        ])
        board = HB6DBoard.from_array(squares)
        # Make sure the board isn't filled (which would be a trivial test)
        self.assertGreater(board._cells.sum(), 81)
        board._quick_fill()
        before_repr = repr(board)

        # When
        board._quick_fill()
        after_repr = repr(board)

        # Then
        self.assertEqual(after_repr, before_repr)


class TestConsistencyCheck(unittest.TestCase):

    def test_consistency_check_doesnt_mutate_board(self):
        # Invalid board without candidates in the three empty squares
        # Number 9 in square (1, 2) shouldn't be there (for example)
        squares = np.array([
            [4,    9,    3,    None, 2,    1,    6,    5,    7],
            [None, 6,    7,    3,    4,    5,    8,    2,    1],
            [2,    5,    1,    8,    7,    6,    4,    9,    3],
            [5,    4,    8,    1,    3,    2,    9,    7,    6],
            [7,    2,    9,    5,    6,    4,    1,    3,    8],
            [1,    3,    6,    7,    9,    8,    2,    4,    5],
            [3,    7,    2,    6,    8,    9,    5,    1,    4],
            [8,    1,    4,    2,    5,    3,    7,    6,    9],
            [6,    None, 5,    4,    1,    7,    3,    8,    2],
        ])
        board = HB6DBoard.from_array(squares)
        repr_before = repr(board)

        with self.assertRaises(ConsistencyError) as exc_cm:
            board._check_consistency()
        repr_after = repr(board)

        self.assertIn("Inconsistency found", str(exc_cm.exception))
        # Make sure the `_check_consistency()` method doesn't change the board
        self.assertEqual(repr_after, repr_before)

    def test_square_consistency_check(self):
        """
        Check that _consistency_check() raises when there is no candidate
        number in the top left square.
        """
        squares = np.array([
            [0, 2, 3, 4, 5, 6, 7, 8, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [9, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        board = HB6DBoard.from_array(squares)
        # Nones are for 'no candidate', _row is 0, _col is 0
        _expected_idx = (None, None, 0, 0, 0, 0)

        with self.assertRaises(ConsistencyError) as exc_cm:
            board._check_consistency()

        self.assertEqual(exc_cm.exception._idx, _expected_idx)

    def test_row_consistency_check(self):
        """
        Check that _consistency_check() raises when number 2 has no valid
        place in the fourth row.
        """
        squares = np.array([
            [2, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 4, 5, 6, 7, 8, 9],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
        ])
        board = HB6DBoard.from_array(squares)
        # _num is 1, _row is 3, Nones are for 'no column'
        _expected_idx = (0, 1, 1, 0, None, None)

        with self.assertRaises(ConsistencyError) as exc_cm:
            board._check_consistency()

        self.assertEqual(exc_cm.exception._idx, _expected_idx)

    def test_column_consistency_check(self):
        """
        Check that _consistency_check() raises when number 3 has no valid
        place in the last column.
        """
        squares = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 3, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 5],
            [0, 0, 0, 0, 0, 0, 0, 0, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 0, 0, 0, 0, 0, 0, 0, 9],
        ])
        board = HB6DBoard.from_array(squares)
        # _num is 2, Nones are for 'no row', _col is 8
        _expected_idx = (0, 2, None, None, 2, 2)

        with self.assertRaises(ConsistencyError) as exc_cm:
            board._check_consistency()

        self.assertEqual(exc_cm.exception._idx, _expected_idx)

    def test_box_consistency_check(self):
        """
        Check that _consistency_check() raises when number 4 has no valid
        place in the middle box.
        """
        squares = np.array([
            [0, 0, 0, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 7, 8, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0],
        ])
        board = HB6DBoard.from_array(squares)
        # _num is 3, _boxrow is 1, _boxcol is 1
        # Nones are for 'no _subrow or _subcol'
        _expected_idx = (1, 0, 1, None, 1, None)

        with self.assertRaises(ConsistencyError) as exc_cm:
            board._check_consistency()

        self.assertEqual(exc_cm.exception._idx, _expected_idx)

    def test_consistency_check_for_valid_board(self):
        # A valid sudoku board
        squares = np.array([
            [4,    None, 3,    None, 2,    1,    6,    5,    7],
            [None, 6,    7,    3,    4,    5,    8,    2,    1],
            [2,    5,    1,    8,    7,    6,    4,    9,    3],
            [5,    4,    8,    1,    3,    2,    9,    7,    6],
            [7,    2,    9,    5,    6,    4,    1,    3,    8],
            [1,    3,    6,    7,    9,    8,    2,    4,    5],
            [3,    7,    2,    6,    8,    9,    5,    1,    4],
            [8,    1,    4,    2,    5,    3,    7,    6,    9],
            [6,    None, 5,    4,    1,    7,    3,    8,    2],
        ])
        board = HB6DBoard.from_array(squares)
        repr_before = repr(board)

        board._check_consistency()
        repr_after = repr(board)

        # No errors
        # Also, ensure candidates are the same in every square
        self.assertEqual(repr_after, repr_before)

    def test_consistency_check_doesnt_always_raise(self):
        """
        This test demonstrates that the `_check_consistency()` method
        doesn't necessarily raise for an inconsistent board.
        """
        # Create a sudoku board that is invalid, but in a non-obvious way
        # In square (2, 8) neither of the two candidates (4 and 9) lead
        # to a valid solution (so the board has no solution), but this is
        # not discovered by `_consistency_check()`.
        squares = [
            [4, 1, 7, 3, 6, 9, 8, 2,    5],
            [2, 3, 6, 1, 5, 8, 7, None, 0],
            [0, 5, 0, 7, 2, 4, 0, 1,    0],
            [0, 2, 5, 4, 3, 7, 1, 6,    0],
            [0, 0, 1, 0, 8, 0, 4, 0,    0],
            [0, 4, 0, 0, 1, 0, 0, 0,    0],
            [0, 0, 2, 6, 4, 3, 5, 7,    1],
            [5, 0, 3, 2, 0, 1, 0, 0,    0],
            [1, 0, 4, 8, 0, 5, 0, 0,    0],
        ]
        # Try the first candidate number: 4
        board_1 = HB6DBoard.from_array(squares)
        board_1.insert(4, 2, 8)
        with self.assertRaises(ConsistencyError):
            board_1._quick_fill()
            board_1._check_consistency()
        # Try the second candidate number: 9
        board_1 = HB6DBoard.from_array(squares)
        board_1.insert(9, 2, 8)
        with self.assertRaises(ConsistencyError):
            board_1._quick_fill()
            board_1._check_consistency()

        # Given
        board = HB6DBoard.from_array(squares)
        # Make sure that there are no other candidates
        self.assertEqual(board.candidates(2, 8), [4, 9])

        # When
        board._check_consistency()

        # Then
        # No errors


class TestFirstEmptySquare(unittest.TestCase):

    def test_first_empty_square_raises(self):
        """
        Check that a completely solved board doesn't have a "first empty
        square".
        """
        # Board is already filled
        squares = np.array([
            [4, 8, 3, 9, 2, 1, 6, 5, 7],
            [9, 6, 7, 3, 4, 5, 8, 2, 1],
            [2, 5, 1, 8, 7, 6, 4, 9, 3],
            [5, 4, 8, 1, 3, 2, 9, 7, 6],
            [7, 2, 9, 5, 6, 4, 1, 3, 8],
            [1, 3, 6, 7, 9, 8, 2, 4, 5],
            [3, 7, 2, 6, 8, 9, 5, 1, 4],
            [8, 1, 4, 2, 5, 3, 7, 6, 9],
            [6, 9, 5, 4, 1, 7, 3, 8, 2],
        ])
        board = HB6DBoard.from_array(squares)

        with self.assertRaises(ValueError) as exc_cm:
            board._first_empty_square()

        self.assertIn("No empty square", str(exc_cm.exception))

    def test_first_empty_square_raises_invalid_board(self):
        # Invalid board without candidates in the three empty squares
        # Number 9 in square (1, 2) shouldn't be there (for example)
        squares = np.array([
            [4,    9,    3,    None, 2,    1,    6,    5,    7],
            [None, 6,    7,    3,    4,    5,    8,    2,    1],
            [2,    5,    1,    8,    7,    6,    4,    9,    3],
            [5,    4,    8,    1,    3,    2,    9,    7,    6],
            [7,    2,    9,    5,    6,    4,    1,    3,    8],
            [1,    3,    6,    7,    9,    8,    2,    4,    5],
            [3,    7,    2,    6,    8,    9,    5,    1,    4],
            [8,    1,    4,    2,    5,    3,    7,    6,    9],
            [6,    None, 5,    4,    1,    7,    3,    8,    2],
        ])
        board = HB6DBoard.from_array(squares)

        with self.assertRaises(ValueError) as exc_cm:
            board._first_empty_square()

        # Even though the three squares are empty, they have no valid
        # candidate numbers, so an exception is raised
        self.assertIn("No empty square", str(exc_cm.exception))

    def test_first_empty_square(self):
        # A board that has an empty square (with valid candidate numbers)
        squares = np.array([
            [6,    None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, None, None, None, None, None, None, None, None],  # noqa: E241
            [None, 5,    None, None, None, None, None, None, None],  # noqa: E241
            [None, 4,    None, None, None, None, None, None, None],  # noqa: E241
            [None, 3,    None, None, None, None, None, None, None],  # noqa: E241
            [None, 2,    None, None, None, None, None, None, None],  # noqa: E241
            [None, 1,    None, None, None, None, None, None, None],  # noqa: E241
        ])
        board = HB6DBoard.from_array(squares)
        # Candidate numbers are 7, 8 and 9
        _expected_candidates = [(2, 2, 2), (0, 1, 2)]
        # Square is in row 1, column 2
        _expected_square = (0, 0, 0, 1)

        _candidates, _square = board._first_empty_square()

        np.testing.assert_array_equal(_candidates, _expected_candidates)
        np.testing.assert_array_equal(_square, _expected_square)


class TestRecursiveSolve(unittest.TestCase):

    def test_recursive_solve_filled_board(self):
        # Board is already filled
        squares = np.array([
            [4, 8, 3, 9, 2, 1, 6, 5, 7],
            [9, 6, 7, 3, 4, 5, 8, 2, 1],
            [2, 5, 1, 8, 7, 6, 4, 9, 3],
            [5, 4, 8, 1, 3, 2, 9, 7, 6],
            [7, 2, 9, 5, 6, 4, 1, 3, 8],
            [1, 3, 6, 7, 9, 8, 2, 4, 5],
            [3, 7, 2, 6, 8, 9, 5, 1, 4],
            [8, 1, 4, 2, 5, 3, 7, 6, 9],
            [6, 9, 5, 4, 1, 7, 3, 8, 2],
        ])
        board = HB6DBoard.from_array(squares)
        expected_str = (
            "4 8 3 | 9 2 1 | 6 5 7\n"
            "9 6 7 | 3 4 5 | 8 2 1\n"
            "2 5 1 | 8 7 6 | 4 9 3\n"
            "---------------------\n"
            "5 4 8 | 1 3 2 | 9 7 6\n"
            "7 2 9 | 5 6 4 | 1 3 8\n"
            "1 3 6 | 7 9 8 | 2 4 5\n"
            "---------------------\n"
            "3 7 2 | 6 8 9 | 5 1 4\n"
            "8 1 4 | 2 5 3 | 7 6 9\n"
            "6 9 5 | 4 1 7 | 3 8 2\n"
        )

        board._recursive_solve()

        self.assertEqual(str(board), expected_str)

    def test_recursive_solve_invalid_board(self):
        # Invalid board without candidates in the three empty squares
        # Number 9 in square (1, 2) shouldn't be there (for example)
        squares = np.array([
            [4,    9,    3,    None, 2,    1,    6,    5,    7],
            [None, 6,    7,    3,    4,    5,    8,    2,    1],
            [2,    5,    1,    8,    7,    6,    4,    9,    3],
            [5,    4,    8,    1,    3,    2,    9,    7,    6],
            [7,    2,    9,    5,    6,    4,    1,    3,    8],
            [1,    3,    6,    7,    9,    8,    2,    4,    5],
            [3,    7,    2,    6,    8,    9,    5,    1,    4],
            [8,    1,    4,    2,    5,    3,    7,    6,    9],
            [6,    None, 5,    4,    1,    7,    3,    8,    2],
        ])

        board = HB6DBoard.from_array(squares)

        with self.assertRaises(ConsistencyError):
            board._recursive_solve()

    def test_recursive_solve_changes_invalid_board(self):
        # Invalid board with no possible candidate in the top left square
        squares = np.array([
            [0, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ])
        board = HB6DBoard.from_array(squares)
        expected_repr = (
            ". . . | . 2 . | . . 3  . . . | . . . | . . .  . . . | . . . | . . .\n"  # noqa: E501
            ". . . | . . . | . . .  4 . . | . 5 . | . . 6  . . . | . . . | . . .\n"  # noqa: E501
            ". . . | . . . | . . .  . . . | . . . | . . .  7 . . | . 8 . | . . 9\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            "1 . . | . . . | . . .  . 2 3 | . 2 3 | . 2 3  . 2 3 | . 2 3 | . 2 3\n"  # noqa: E501
            ". . . | 4 5 6 | 4 5 6  . . . | . . . | . . .  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            ". . . | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  . . . | . . . | . . .\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            ". . . | . . . | . . .  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  . . . | . . . | . . .  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  . . . | . . . | . . .\n"  # noqa: E501
            "\n"
            ". 2 3 | 1 . 3 | 1 2 .  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  . 5 6 | 4 . 6 | 4 5 .  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  . 8 9 | 7 . 9 | 7 8 .\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            ". 2 3 | 1 . 3 | 1 2 .  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  . 5 6 | 4 . 6 | 4 5 .  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  . 8 9 | 7 . 9 | 7 8 .\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            ". 2 3 | 1 . 3 | 1 2 .  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  . 5 6 | 4 . 6 | 4 5 .  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  . 8 9 | 7 . 9 | 7 8 .\n"  # noqa: E501
            "\n"
            ". 2 3 | 1 . 3 | 1 2 .  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  . 5 6 | 4 . 6 | 4 5 .  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  . 8 9 | 7 . 9 | 7 8 .\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            ". 2 3 | 1 . 3 | 1 2 .  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  . 5 6 | 4 . 6 | 4 5 .  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  . 8 9 | 7 . 9 | 7 8 .\n"  # noqa: E501
            "---------------------  ---------------------  ---------------------\n"  # noqa: E501
            ". 2 3 | 1 . 3 | 1 2 .  1 2 3 | 1 2 3 | 1 2 3  1 2 3 | 1 2 3 | 1 2 3\n"  # noqa: E501
            "4 5 6 | 4 5 6 | 4 5 6  . 5 6 | 4 . 6 | 4 5 .  4 5 6 | 4 5 6 | 4 5 6\n"  # noqa: E501
            "7 8 9 | 7 8 9 | 7 8 9  7 8 9 | 7 8 9 | 7 8 9  . 8 9 | 7 . 9 | 7 8 .\n"  # noqa: E501
        )

        with self.assertRaises(ConsistencyError):
            board._recursive_solve()

        # Some candidates are removed despite the board being invalid
        self.assertEqual(repr(board), expected_repr)

    def test_recursive_solve(self):
        # Given
        squares = np.array([
            [0, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 9, 0, 7],
            [0, 7, 6, 0, 2, 0, 3, 0, 0],
            [0, 0, 0, 0, 7, 0, 0, 3, 0],
            [0, 0, 1, 2, 0, 5, 4, 0, 0],
            [0, 9, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 5, 0, 6, 0, 2, 9, 0],
            [6, 0, 4, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 5, 0],
        ])
        board = HB6DBoard.from_array(squares)
        # Make sure _quick_fill() doesn't solve the board
        # (which would be a trivial test)
        board._quick_fill()
        self.assertGreater(board._cells.sum(), 81)
        board = HB6DBoard.from_array(squares)
        expected_str = (
            "1 8 3 | 7 9 6 | 5 4 2\n"
            "4 5 2 | 3 1 8 | 9 6 7\n"
            "9 7 6 | 5 2 4 | 3 1 8\n"
            "---------------------\n"
            "2 4 8 | 6 7 9 | 1 3 5\n"
            "3 6 1 | 2 8 5 | 4 7 9\n"
            "5 9 7 | 1 4 3 | 8 2 6\n"
            "---------------------\n"
            "8 3 5 | 4 6 7 | 2 9 1\n"
            "6 2 4 | 9 5 1 | 7 8 3\n"
            "7 1 9 | 8 3 2 | 6 5 4\n"
        )

        # When
        board._recursive_solve()

        # Then
        self.assertEqual(str(board), expected_str)

    def test_recursive_solve_strange_board(self):
        """
        See `test_consistency_check_doesnt_always_raise`.
        """
        # Recursively solving this board happens to exercise the rare case
        # when the `_recursive_solve()` method raises because of an
        # inconsistency that isn't detected by `_consistency_check()`.
        squares = [
            [4,    1,    7,    3,    6,    9,    8,    2,    5],
            [2,    3,    6,    1,    5,    8,    7,    None, None],
            [None, 5,    None, 7,    2,    4,    None, 1,    None],
            [None, 2,    5,    4,    3,    7,    1,    6,    None],
            [None, None, 1,    None, 8,    None, 4,    None, None],
            [None, 4,    None, None, 1,    None, None, None, None],
            [None, None, 2,    6,    4,    3,    5,    7,    1],
            [5,    None, 3,    2,    None, 1,    None, None, None],
            [1,    None, 4,    8,    None, 5,    None, None, None],
        ]
        board = HB6DBoard.from_array(squares)

        with self.assertRaises(ConsistencyError) as exc_cm:
            board._recursive_solve()
        self.assertEqual("No solution found.", str(exc_cm.exception))


class TestSolve(unittest.TestCase):

    def test_solve_invalid_board(self):
        # Invalid board without candidates in the three empty squares
        # Number 9 in square (1, 2) shouldn't be there (for example)
        squares = np.array([
            [4,    9,    3,    None, 2,    1,    6,    5,    7],
            [None, 6,    7,    3,    4,    5,    8,    2,    1],
            [2,    5,    1,    8,    7,    6,    4,    9,    3],
            [5,    4,    8,    1,    3,    2,    9,    7,    6],
            [7,    2,    9,    5,    6,    4,    1,    3,    8],
            [1,    3,    6,    7,    9,    8,    2,    4,    5],
            [3,    7,    2,    6,    8,    9,    5,    1,    4],
            [8,    1,    4,    2,    5,    3,    7,    6,    9],
            [6,    None, 5,    4,    1,    7,    3,    8,    2],
        ])

        board = HB6DBoard.from_array(squares)

        with self.assertRaises(ConsistencyError):
            board.solve()
