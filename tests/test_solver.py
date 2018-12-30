import unittest

import numpy as np

from solver import Solver


class TestSolver(unittest.TestCase):

    def test_solver_init_type_invalid(self):
        # List of lists, instead of 2D array
        array = [[0, 1, 2, 3], [2, 3, 0, 1], [1, 0, 3, 2], [3, 2, 1, 0]]

        with self.assertRaises(TypeError):
            Solver(array)

    def test_solver_init(self):
        array = np.array(
            [[0, 1, 2, 3], [2, 3, 0, 1], [1, 0, 3, 2], [3, 2, 1, 0]])
        expected = np.array([
            [
                [True, False, False, False],
                [False, False, True, False],
                [False, True, False, False],
                [False, False, False, True],
            ],
        ])

        solver = Solver(array)

        # Then
        self.assertEqual(solver._side_length, 4)

        self.assertEqual(solver.board.ndim, 3)
        self.assertEqual(solver.board.shape, (4, 4, 4))
        # self.assertEqual(solver._board[0], expected[0])
