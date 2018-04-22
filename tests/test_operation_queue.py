import unittest

from operation_queue import OperationQueue

class TestOperationQueue(unittest.TestCase):
    def test_operation_queue_init(self):
        # Given
        side_len = 9
        expected_operation_count = 4*9*9

        # When
        operations = OperationQueue(side_len)
        operation_count = len(operations._deque)

        # Then
        self.assertEqual(expected_operation_count, operation_count)

    def test_operation_queue
