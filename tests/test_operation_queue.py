import unittest

from operation import Operation
from operation_queue import OperationQueue


class TestOperationQueue(unittest.TestCase):
    def test_operation_queue_init(self):
        # Given
        expected_operation_count = 4*9*9

        # When
        operations = OperationQueue(9)
        operation_count = len(operations._deque)

        # Then
        self.assertEqual(expected_operation_count, operation_count)

    def test_operation_queue_get_head(self):
        # Given
        expected_operation = Operation('dig', 0, 0)

        # When
        operation = OperationQueue(4).get_head()

        # Then
        self.assertEqual(operation, expected_operation)

    def test_operation_queue_requeue_every_element(self):
        # Given
        operations = OperationQueue(4)
        expected_operations = OperationQueue(4)

        # When
        for i in range(4*16):
            operations.requeue()

        # Then
        self.assertEqual(expected_operations, operations)

    def test_operation_queue_remove_rearrange_single_operation(self):
        # Given
        operations = OperationQueue(1)

        # When
        operations.remove_rearrange(0, 0, 0, 1, 1)

        # Then
        self.assertTrue(operations.empty())

    def test_operation_queue_remove_rearrange_len(self):
        # Given
        operations = OperationQueue(4)
        expected_len = 4*16 - 4

        # When
        operations.remove_rearrange(0, 0, 0, 2, 2)

        # Then
        self.assertEqual(len(operations._deque), expected_len)
