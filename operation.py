from indexing import boxindex, rows_cols


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
        return f"<Operation(" \
               f"'{self.finds}', " \
               f"({self.indices[0]}, {self.indices[1]})" \
               f")>"

    def is_peer_of(self, dig, row, col, box_height, box_width):
        """
        Decide if this operation is a peer of (dig, row, col), i.e. whether
        it should be prioritised after _add(dig, row, col).
        """
        if self.finds == 'dig':
            # same box or same row or same col
            this_row = self.indices[0]
            this_col = self.indices[1]
            this_box = boxindex(this_row, this_col, box_height, box_width)
            box = boxindex(row, col, box_height, box_width)
            return this_row == row or this_col == col or this_box == box
        elif self.finds == 'row':
            this_dig = self.indices[0]
            this_col = self.indices[1]
            return this_dig == dig or this_col == col
        elif self.finds == 'col':
            this_dig = self.indices[0]
            this_row = self.indices[1]
            return this_dig == dig or this_row == row
        elif self.finds == 'pos':
            this_dig = self.indices[0]
            this_box = self.indices[1]
            this_row_slice, this_col_slice = rows_cols(this_box, box_height,
                                                       box_width)
            box = boxindex(row, col, box_height, box_width)
            row_slice, col_slice = rows_cols(row, col, box_height, box_width)
            return (this_box == box
                    or (this_dig == dig and this_row_slice == row_slice)
                    or (this_dig == dig and this_col_slice == col_slice))

        raise ValueError
