from indexing import boxindex


class Operation:
    def __init__(self, s, i, j):
        self.finds = s
        self.indices = (i, j)

    def __repr__(self):
        return f"<{self.finds} {self.indices}, operation.Operation object>"

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
