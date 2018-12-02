import numpy as np


_NO_CANDIDATE_STR = '.'

_REPR_HORIZONTAL_SEP_BIG = '\n\n'

_REPR_HORIZONTAL_SEP_MEDIUM = (
    '\n---------------------  ---------------------  ---------------------\n'
)

_REPR_HORIZONTAL_SEP_SMALL = '\n'

_REPR_VERTICAL_SEP_BIG = '  '

_REPR_VERTICAL_SQUARE_MEDIUM = ' | '

_REPR_VERTICAL_SEP_SMALL = ' '

# Dimensions of the HB6DBoard's underlying array
_SHAPE = (3,) * 6

_STR_HORIZONTAL_SEP_MEDIUM = (
    '\n---------------------\n'
)

_STR_HORIZONTAL_SEP_SMALL = '\n'

_STR_VERTICAL_SQUARE_MEDIUM = ' | '

_STR_VERTICAL_SEP_SMALL = ' '


class HB6DBoard(object):
    """
    Data structure for storing and solving a sudoku board.
    """

    def __init__(self):
        # Dimensions of the underlying 6D boolean array
        self._shape = _SHAPE
        self._cells = np.full(shape=self._shape, fill_value=True, dtype=bool)

    def _num_row_col_to_idx(self, _num, _row, _col):
        # _num_div3, _num_mod3 = divmod(_num, 3)
        # _boxrow, _subrow = divmod(_row, 3)
        # _boxcol, _subcol = divmod(_col, 3)
        # _idx = (_num_div3, _num_mod3, _boxrow, _subrow, _boxcol, _subcol)
        return (*divmod(_num, 3), *divmod(_row, 3), *divmod(_col, 3))

    def _idx_to_num_row_col(self, _idx):
        """
        Return the number, row, and column that is represented by the cell
        with the given coordinates.

        Parameters
        ----------
        _idx : numpy.ndarray
            Zero-based coordinates referring to a single cell.

        Returns
        -------
        _num : int between 0 and 8 inclusive
            Candidate referenced by the cell with the given index. Zero-based.
        _row : int between 0 and 8 inclusive
            Row referenced by the the cell with the given index. Zero-based.
        _col : int between 0 and 8 inclusive
            Column referenced by the cell with the given index. Zero-based.
        """
        # _num = 3 * _idx[0] + _idx[1]
        # _row = 3 * _idx[2] + _idx[3]
        # _col = 3 * _idx[4] + _idx[5]
        return _idx[0]*3 + _idx[1], _idx[2]*3 + _idx[3], _idx[4]*3 + _idx[5]

    def __repr__(self):
        board_repr = ''

        # Append three box rows to `board_repr`
        for boxrow in range(3):
            # Append three rows to `board_repr`
            for subrow in range(3):
                # Append three lines to `board_repr`
                for num_div3 in range(3):
                    # Append a single line to `board_repr`
                    for boxcol in range(3):
                        # Append three squares to `board_repr`
                        for subcol in range(3):
                            # Append three cells to `board_repr`
                            for num_mod3 in range(3):
                                # Append a single cell to `board_repr`
                                _idx = (
                                    num_div3, num_mod3,  # number
                                    boxrow, subrow,  # row
                                    boxcol, subcol,  # column
                                )
                                _num, _, _ = self._idx_to_num_row_col(_idx)
                                if self._cells[_idx]:
                                    # Convert the number to one-based indexing
                                    str_value = str(_num + 1)
                                else:
                                    str_value = _NO_CANDIDATE_STR
                                board_repr += str_value

                                # Append a vertical cell separator if needed
                                if num_mod3 != 2:
                                    board_repr += _REPR_VERTICAL_SEP_SMALL

                            # Append a vertical square separator if this is
                            # not the last column of the box
                            if subcol != 2:
                                board_repr += _REPR_VERTICAL_SQUARE_MEDIUM

                        # Append a vertical box separator if this is not the
                        # last box column
                        if boxcol != 2:
                            board_repr += _REPR_VERTICAL_SEP_BIG

                    # Append a horizontal cell separator if this is not the
                    # last line of the square
                    if num_div3 != 2:
                        board_repr += _REPR_HORIZONTAL_SEP_SMALL

                # Append a horizontal square separator if this is not the
                # last row in the box
                if subrow != 2:
                    board_repr += _REPR_HORIZONTAL_SEP_MEDIUM

            # Append a horizontal box separator if this is not the last box row
            if boxrow != 2:
                board_repr += _REPR_HORIZONTAL_SEP_BIG

        # Append a newline to the end
        board_repr += '\n'

        return board_repr

    def _put(self, _idx):
        """
        Insert a number into the given square.

        Parameters
        ----------
        _idx : tuple of ints of shape (6,)
            Coordinates representing a single candidate number and a square.

            Zero-based indices.

        Raises
        ------
        ValueError
            If the number is not a candidate in the given square.
        """
        if not self._cells[_idx]:
            msg = "Number {} is not a candidate in square ({}, ())."
            _num, _row, _col = self._idx_to_num_row_col(_idx)
            raise ValueError(msg.format(_num, _row, _col))

        _num_div3, _num_mod3, _boxrow, _subrow, _boxcol, _subcol = _idx

        # Set square peers to False
        self._cells[:, :, _boxrow, _subrow, _boxcol, _subcol] = False
        # Set numcol peers to False
        self._cells[_num_div3, _num_mod3, :, :, _boxcol, _subcol] = False
        # Set numrow peers to False
        self._cells[_num_div3, _num_mod3, _boxrow, _subrow, :, :] = False
        # Set numbox peers to False
        self._cells[_num_div3, _num_mod3, _boxrow, :, _boxcol, :] = False

        # Set the cell itself to True
        self._cells[_idx] = True

    @classmethod
    def from_array(cls, array):
        """
        Create a HB6DBoard instance from the given 2D array.

        Parameters
        ----------
        array : numpy.ndarray of int or None and of shape (9, 9)
            Nine-by-nine array of fill values for each square. None values
            correspond to empty squares.

            Candidate numbers are one-based (i.e. 1 to 9).

        Raises
        ------
        ValueError
        """
        obj = cls()

        for _row, row in enumerate(array):
            for _col, number in enumerate(row):
                if number in range(1, 10):
                    _num = number - 1
                    _idx = obj._num_row_col_to_idx(_num, _row, _col)
                    try:
                        obj._put(_idx)
                    except ValueError:
                        msg = "Clash found during instantiation: {} ({}, {})."
                        raise ValueError(msg.format(number, _row+1, _col+1))

        return obj

    def candidates(self, row, column):
        """
        Valid candidate numbers in the given square in increasing order.

        Parameters
        ----------
        row : int between 1 and 9
        column : int between 1 and 9

        Returns
        -------
        numbers : list of int
            Numbers that are valid candidates in the given square. One-based.
        """
        boxrow, subrow = divmod(row - 1, 3)
        boxcol, subcol = divmod(column - 1, 3)
        cells = self._cells[:, :, boxrow, subrow, boxcol, subcol].flat
        numbers = [
            idx+1
            for idx, is_candidate in enumerate(cells)
            if is_candidate
        ]
        return numbers

    def __str__(self):
        result = ''

        # Append three box rows to `result`
        for boxrow in range(3):
            # Append three lines to `result`
            for subrow in range(3):
                row = 3 * boxrow + subrow + 1
                # Append three box columns to `result`
                for boxcol in range(3):
                    # Append three columns to `result`
                    for subcol in range(3):
                        # Append a single character to `result`
                        column = 3 * boxcol + subcol + 1
                        numbers = self.candidates(row, column)
                        if len(numbers) == 1:
                            number, = numbers
                            result += str(number)
                        else:
                            result += _NO_CANDIDATE_STR

                        # Append a vertical square separator if this is not
                        # the last column of the box
                        if subcol != 2:
                            result += _STR_VERTICAL_SEP_SMALL

                    # Append a vertical box separator if this is not the last
                    # box column
                    if boxcol != 2:
                        result += _STR_VERTICAL_SQUARE_MEDIUM

                # Append a horizontal row separator if this is not the last
                # subrow in the box
                if subrow != 2:
                    result += _STR_HORIZONTAL_SEP_SMALL

            # Append a horizontal box separator if this is not the last box row
            if boxrow != 2:
                result += _STR_HORIZONTAL_SEP_MEDIUM

        # Append a newline to the end
        result += '\n'

        return result

    def insert(self, number, row, column):
        _idx = self._num_row_col_to_idx(number - 1, row - 1, column - 1)
        try:
            self._put(_idx)
        except ValueError:
            msg = ""
            raise ValueError(msg)

    def _quick_fill(self):

        # Repeat until there are definitely no more insertions
        for _ in range(81):

            for _linear_idx in range(np.prod(self._shape[:4])):

                # Fix four out of the six coordinates
                _p, _q, _r, _s = np.unravel_index(_linear_idx, self._shape[:4])

                # Inspect a single square
                x, y = self._cells[:, :, _p, _q, _r, _s].nonzero()
                if len(x) == 1:
                    self._put((x[0], y[0], _p, _q, _r, _s))

                # Inspect a number in a single row
                x, y = self._cells[_p, _q, _r, _s, :, :].nonzero()
                if len(x) == 1:
                    self._put((_p, _q, _r, _s, x[0], y[0]))

                # Inspect a number in a single column
                x, y = self._cells[_p, _q, :, :, _r, _s].nonzero()
                if len(x) == 1:
                    self._put((_p, _q, x[0], y[0], _r, _s))

                # Inspect a number in a single box
                x, y = self._cells[_p, _q, _r, :, _s, :].nonzero()
                if len(x) == 1:
                    self._put((_p, _q, _r, x[0], _s, y[0]))
