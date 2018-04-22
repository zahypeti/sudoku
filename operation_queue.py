from collections import deque

from indexing import boxindex
from operation import Operation


class OperationQueue:
    def __init__(self, side_length):
        # Fill in queue with all 4*n2 possible operations in order
        self._deque = deque([], maxlen=4*side_length**2)
        double_loop = [(i, j)
                       for i in range(side_length) for j in range(side_length)]
        for i, j in double_loop:
            for finds in ['dig', 'row', 'col', 'pos']:
                operation = Operation(finds, i, j)
                self._deque.append(operation)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        result = 'OperationQueue object:\n'
        for op in self._deque:
            result += (' ' + op.__str__() + '\n')
        return result

    def empty(self):
        return len(self._deque) == 0

    def get_head(self):
        return self._deque[0]

    def requeue(self):
        """ Dequeue head and enqueue at the end. """
        self._deque.rotate(-1)

    def remove_rearrange(self, dig, row, col, box_height, box_width):
        """
        Pop the next item from the queue, remove similar operations (max 3, if
        applicable), and rearrange the remaining ones.
        """

        # Remove next operation from the head
        del self._deque[0]

        # Remove max 3 similar operations
        try:
            self._deque.remove(Operation('dig', row, col))
        except ValueError:
            pass
        try:
            self._deque.remove(Operation('row', dig, col))
        except ValueError:
            pass
        try:
            self._deque.remove(Operation('col', dig, row))
        except ValueError:
            pass
        try:
            box = boxindex(row, col, box_height, box_width)
            self._deque.remove(Operation('pos', dig, box))
        except ValueError:
            pass

        # Create peer and non-peer queues
        peers = deque()
        others = deque()
        while 0 < len(self._deque):
            item = self._deque.popleft()
            if item.is_peer_of(dig, row, col, box_height, box_width):
                peers.append(item)
            else:
                others.append(item)

        # Enqueue peers then non-peers to self._deque
        self._deque += (peers + others)

