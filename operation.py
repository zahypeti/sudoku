from indexing import boxindex


class Operation:
    def __init__(self, s, i, j):
        self.finds = s
        self.indices = (i, j)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"<Operation({self.finds}, " \
               f"({self.indices[0]}, {self.indices[1]})>"

    def is_peer_of(self, dig, row, col, box_height, box_width):
        """
        Decide if slf is a peer of (dig, row, col), i.e. whether they share a
        row, column, box or digit.
        """
        if self.finds == 'dig':
            return (row, col) == self.indices
        elif self.finds == 'row':
            return (dig, col) == self.indices
        elif self.finds == 'col':
            return (dig, row) == self.indices
        elif self.finds == 'pos':
            box = boxindex(row, col, box_height, box_width)
            return (dig, box) == self.indices
        raise ValueError
