import unittest

from operation import Operation


class TestOperation(unittest.TestCase):
    def test_operation_init(self):
        # Given
        s = 'dig'
        i, j = 1, 1
        expected_finds = 'dig'
        expected_indices = (1, 1)

        # When
        operation = Operation(s, i, j)

        # Then
        self.assertEqual(expected_finds, operation.finds)
        self.assertEqual(expected_indices, operation.indices)

    def test_operation_peer(self):
        # Given
        s = 'dig'
        i, j = 1, 1
        dig, row, col = 1, 1, 1
        box_height, box_width = 3, 3

        # When
        operation = Operation(s, i, j)
        result = operation.is_peer_of(dig, row, col, box_height, box_width)

        # Then
        self.assertTrue(result)

    def test_operation_peer_rectangular(self):
        # Given
        s = 'pos'
        i, j = 10, 20
        dig, row, col = 1, 1, 1
        box_height, box_width = 3, 7

        # When
        operation = Operation(s, i, j)
        result = operation.is_peer_of(dig, row, col, box_height, box_width)

        # Then
        self.assertFalse(result)
