import unittest

from operation import Operation
from operation_queue import OperationQueue


class TestOperationQueue(unittest.TestCase):
    def test_operation_queue_init(self):
        # Given
        expected_operation_count = 4*9*9

        # When
        operations = OperationQueue(None, 3, 3)
        operation_count = len(operations._deque)

        # Then
        self.assertEqual(expected_operation_count, operation_count)

    def test_operation_queue_equality(self):
        # When
        queue_a1 = OperationQueue([
            Operation('col', 0, 0),
            Operation('col', 0, 1),
        ], 2, 2)
        queue_a2 = OperationQueue([
            Operation('col', 0, 0),
            Operation('col', 0, 1),
        ], 2, 2)
        queue_b = OperationQueue(None, 2, 2)

        # Then
        self.assertEqual(queue_a1, queue_a2)
        self.assertNotEqual(queue_a1, queue_b)
        self.assertNotEqual(queue_a2, queue_b)

    def test_operation_queue_empty(self):
        # Given
        operations = OperationQueue([], 2, 2)

        # When & Then
        self.assertTrue(operations.empty())

    def test_operation_queue_get_head_of_empty(self):
        # Given
        operations = OperationQueue([], 3 ,3)

        # When & Then
        with self.assertRaises(IndexError):
            operations.get_head()

    def test_operation_queue_get_head(self):
        # Given
        expected_operation = Operation('dig', 0, 0)

        # When
        operation = OperationQueue(None, 2, 2).get_head()

        # Then
        self.assertEqual(operation, expected_operation)

    def test_operation_queue_requeue_every_element(self):
        # Given
        operations = OperationQueue(None, 2, 2)
        expected_operations = OperationQueue(None, 2, 2)

        # When
        for i in range(4*16):
            operations.requeue()

        # Then
        self.assertEqual(expected_operations, operations)

    def test_operation_queue_remove_rearrange_single_operation(self):
        # Given
        operations = OperationQueue(None, 1, 1)

        # When
        operations.remove_rearrange(0, 0, 0)

        # Then
        self.assertTrue(operations.empty())

    def test_operation_queue_remove_rearrange_len(self):
        # Given
        operations = OperationQueue(None, 2, 2)
        expected_len = 4*16 - 4

        # When
        operations.remove_rearrange(0, 0, 0)

        # Then
        self.assertEqual(len(operations._deque), expected_len)

    def test_operation_queue_arbitrary_remove_rearrange(self):
        # Given
        operation_list = [Operation('dig', 0, 0), Operation('row', 1, 1)]
        operations = OperationQueue(operation_list, 1, 2)
        expected_operations = OperationQueue([Operation('row', 1, 1)], 1, 2)

        # When
        operations.remove_rearrange(0, 0, 0)

        # Then
        self.assertEqual(expected_operations, operations)
