import unittest

from solver import Solver


class TestSolver(unittest.TestCase):

    def test_solver_init_type_invalid(self):
        # List of lists, instead of 2D array
        array = [[0, 1, 2, 3], [2, 3, 0, 1], [1, 0, 3, 2], [3, 2, 1, 0]]

        with self.assertRaises(TypeError):
            Solver(array)
