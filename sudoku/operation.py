from sudoku.indexing import boxindex, rows_cols


ROW_COLUMN = 'square'
DIGIT_ROW = 'digrow'
DIGIT_COLUMN = 'digcol'
DIGIT_BOX = 'digbox'


class Operation:

    def __init__(self, s, i, j):
        """
        An operation that inspects location (i,j) in the given coordinate
        system s.

        Parameters
        ----------
        s : str
            One of the module level strings defined above.
        i, j : int
            Zero-based positions in the given frame of reference.
        """
        self.inspects = s
        self.indices = (i, j)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.inspects == other.inspects
                   and self.indices == other.indices)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        """
        A short representation of this Operation instance of the form
        Operation('digcol', 0, 1).
        """
        return "Operation('{}', {}, {})".format(
            self.inspects, self.indices[0], self.indices[1])

    def is_peer_of(self, dig, row, col, box_height, box_width):
        """
        Decide if this operation is a peer of (dig, row, col), i.e. whether
        it should be prioritised after _add(dig, row, col).
        """
        if self.inspects == ROW_COLUMN:
            # same box or same row or same col
            this_row = self.indices[0]
            this_col = self.indices[1]
            this_box = boxindex(this_row, this_col, box_height, box_width)
            box = boxindex(row, col, box_height, box_width)
            return this_row == row or this_col == col or this_box == box
        elif self.inspects == DIGIT_ROW:
            this_dig = self.indices[0]  # some are primary
            this_row = self.indices[1]
            return this_dig == dig or this_row == row
        elif self.inspects == DIGIT_COLUMN:
            this_dig = self.indices[0]  # some are primary
            this_col = self.indices[1]
            return this_dig == dig or this_col == col
        elif self.inspects == DIGIT_BOX:
            this_dig = self.indices[0]
            this_box = self.indices[1]
            this_row_slice, this_col_slice = rows_cols(this_box, box_height,
                                                       box_width)
            box = boxindex(row, col, box_height, box_width)
            row_slice, col_slice = rows_cols(row, col, box_height, box_width)
            return (this_box == box or
                    (this_dig == dig and this_row_slice == row_slice) or#primry
                    (this_dig == dig and this_col_slice == col_slice)) #primary

        raise ValueError
