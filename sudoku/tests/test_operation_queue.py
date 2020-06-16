from collections import deque
import unittest

from sudoku.operation import (
    DIGIT_BOX, DIGIT_COLUMN, DIGIT_ROW, Operation, ROW_COLUMN,
)
from sudoku.operation_queue import OperationQueue


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
            Operation(DIGIT_ROW, 0, 0),
            Operation(DIGIT_ROW, 0, 1),
        ], 2, 2)
        queue_a2 = OperationQueue([
            Operation(DIGIT_ROW, 0, 0),
            Operation(DIGIT_ROW, 0, 1),
        ], 2, 2)
        queue_b = OperationQueue(None, 2, 2)

        # Then
        self.assertEqual(queue_a1, queue_a2)
        self.assertNotEqual(queue_a1, queue_b)
        self.assertNotEqual(queue_a2, queue_b)

    def test_operation_queue_order_equality(self):
        # When
        queue_a1 = OperationQueue([
            Operation(DIGIT_ROW, 0, 0),
            Operation(DIGIT_ROW, 0, 1),
        ], 2, 2)
        queue_a2 = OperationQueue([
            Operation(DIGIT_ROW, 0, 0),
            Operation(DIGIT_ROW, 0, 1),
        ], 2, 2)
        reverse_queue = OperationQueue([
            Operation(DIGIT_ROW, 0, 1),
            Operation(DIGIT_ROW, 0, 0),
        ], 2, 2)

        # Then
        self.assertEqual(queue_a1, queue_a2)
        self.assertNotEqual(queue_a1, reverse_queue)
        self.assertNotEqual(queue_a2, reverse_queue)

    def test_operation_queue_emptiness(self):
        # Given
        no_operations = OperationQueue([], 2, 2)
        some_operations = OperationQueue()

        # When & Then
        self.assertTrue(no_operations.empty())
        self.assertFalse(some_operations.empty())

    def test_get_head_of_empty_operation_queue(self):
        # Given
        operations = OperationQueue([], 3, 3)

        # When & Then
        with self.assertRaises(IndexError):
            operations.get_head()

    def test_get_head_of_full_operation_queue(self):
        # Given
        expected_operation = Operation(ROW_COLUMN, 0, 0)

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

    def test_requeue_single_operation(self):
        # Given
        result = OperationQueue([
            Operation(DIGIT_COLUMN, 2, 1),
            Operation(ROW_COLUMN, 2, 0),
            Operation(DIGIT_BOX, 2, 1),
        ])
        expected_result = OperationQueue([
            Operation(ROW_COLUMN, 2, 0),
            Operation(DIGIT_BOX, 2, 1),
            Operation(DIGIT_COLUMN, 2, 1),
        ])

        # When
        result.requeue()

        # Then
        self.assertEqual(expected_result, result)

    def test_requeue_empty_operation_queue(self):
        # Given
        operations = OperationQueue([], 2, 2)

        # When
        result = OperationQueue([], 2, 2)
        result.requeue()

        # Then
        self.assertEqual(operations, result)

    def test_deque_iadd(self):
        d = deque('a')
        d += 'bcd'
        self.assertEqual(list(d), list('abcd'))
        d += d
        self.assertEqual(list(d), list('abcdabcd'))

    def test_remove_rearrange_single_operation(self):
        # Given
        operations = OperationQueue(None, 1, 1)

        # When
        operations.remove_rearrange(0, 0, 0)

        # Then
        self.assertTrue(operations.empty())

    def test_remove_rearrange_operation_queue_len(self):
        # Given
        operations = OperationQueue(None, 2, 2)
        expected_len = 4*16 - 4

        # When
        operations.remove_rearrange(0, 0, 0)

        # Then
        self.assertEqual(len(operations._deque), expected_len)

    def test_operation_queue_arbitrary_remove_rearrange(self):
        # Given
        operation_list = [Operation(ROW_COLUMN, 0, 0), Operation(DIGIT_COLUMN, 1, 1)]
        operations = OperationQueue(operation_list, 1, 2)
        expected_operations = OperationQueue([Operation(DIGIT_COLUMN, 1, 1)], 1, 2)

        # When
        operations.remove_rearrange(0, 0, 0)

        # Then
        self.assertEqual(expected_operations, operations)

    def test_remove_rearrange_from_full_operation_queue(self):
        # Given
        operations = OperationQueue([
            Operation(DIGIT_COLUMN, 0, 0),
            Operation(DIGIT_COLUMN, 0, 1),
            Operation(DIGIT_COLUMN, 1, 0),
            Operation(DIGIT_COLUMN, 1, 1),
            Operation(DIGIT_ROW, 0, 0),
            Operation(DIGIT_ROW, 0, 1),
            Operation(DIGIT_ROW, 1, 0),
            Operation(DIGIT_ROW, 1, 1),
            Operation(ROW_COLUMN, 0, 0),
            Operation(ROW_COLUMN, 0, 1),
            Operation(ROW_COLUMN, 1, 0),
            Operation(ROW_COLUMN, 1, 1),
            Operation(DIGIT_BOX, 0, 0),
            Operation(DIGIT_BOX, 0, 1),
            Operation(DIGIT_BOX, 1, 0),
            Operation(DIGIT_BOX, 1, 1),
        ], 1, 2)
        expected = OperationQueue([
            Operation(DIGIT_COLUMN, 0, 1),
            Operation(DIGIT_COLUMN, 1, 0),
            Operation(DIGIT_ROW, 0, 1),
            Operation(DIGIT_ROW, 1, 0),
            Operation(ROW_COLUMN, 0, 1),
            Operation(ROW_COLUMN, 1, 0),
            Operation(DIGIT_BOX, 0, 1),
            Operation(DIGIT_BOX, 1, 0),
            # (0, 0, 0) arranged to the end
            Operation(DIGIT_COLUMN, 0, 0),
            Operation(DIGIT_ROW, 0, 0),
            Operation(ROW_COLUMN, 0, 0),
            Operation(DIGIT_BOX, 0, 0),
        ], 1, 2)

        # When
        operations.remove_rearrange(1, 1, 1)

        # Then
        self.assertEqual(expected, operations)
