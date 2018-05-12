from collections import deque

from indexing import boxindex
from operation import DIGIT_BOX, DIGIT_COLUMN, DIGIT_ROW, Operation, ROW_COLUMN


class OperationQueue:
    def __init__(self, lst=None, box_height=3, box_width=3):
        self.box_height = box_height
        self.box_width = box_width

        side_length = box_height * box_width

        if lst is None:
            # Fill in queue with all 4*n2 possible operations in order
            self._deque = deque([], maxlen=4*side_length**2)
            double_loop = [(i, j)
                           for i in range(side_length)
                           for j in range(side_length)]
            for i, j in double_loop:
                for inspects in [ROW_COLUMN, DIGIT_ROW,
                                 DIGIT_COLUMN,
                                 DIGIT_BOX]:
                    operation = Operation(inspects, i, j)
                    self._deque.append(operation)
        else:
            self._deque = deque(lst, maxlen=4*side_length**2)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        result = '<OperationQueue(box_height={}, box_width={})>'
        return result.format(self.box_height, self.box_width)

    def __str__(self):
        result = 'OperationQueue object:\n'
        for op in self._deque:
            result += (' ' + op.__repr__() + '\n')
        return result

    def empty(self):
        return len(self._deque) == 0

    def get_head(self):
        if self.empty():
            msg = 'OperationQueue is empty.'
            raise IndexError(msg)
        return self._deque[0]

    def requeue(self):
        """
        Dequeue head and enqueue at the end.
        If _deque is empty, requeue() does not affect the OperationQueue.
        """
        self._deque.rotate(-1)

    def remove_rearrange(self, dig, row, col):
        """
        Remove similar operations (those ones that refer to the same square),
        and rearrange the remaining ones. Removes at most 4 operations.
        """

        # Remove similar operations pointing to the same (dig, row, col) triple
        try:
            self._deque.remove(Operation(ROW_COLUMN, row, col))
        except ValueError:
            pass
        try:
            self._deque.remove(Operation(DIGIT_COLUMN, dig, col))
        except ValueError:
            pass
        try:
            self._deque.remove(Operation(DIGIT_ROW, dig, row))
        except ValueError:
            pass
        try:
            box = boxindex(row, col, self.box_height, self.box_width)
            self._deque.remove(Operation(DIGIT_BOX, dig, box))
        except ValueError:
            pass

        # Create peer and non-peer queues
        peers = deque()
        others = deque()
        while 0 < len(self._deque):
            item = self._deque.popleft()
            if item.is_peer_of(dig, row, col, self.box_height, self.box_width):
                peers.append(item)
            else:
                others.append(item)

        # Enqueue peers then non-peers to self._deque
        self._deque += (peers + others)
