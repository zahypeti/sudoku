import numpy as np


_ALPHABET = '123456789'

_HORIZONTAL_BOX_SEP = '=========== =========== ===========\n'

_HORIZONTAL_SQUARE_SEP = '----------- ----------- -----------\n'

_SHAPE = (3, 3, 3, 3, 9)

_TRUE_RECTANGLE = np.ones(shape=(3, 3), dtype=bool)

_TRUE_LINE = np.ones(shape=(9,), dtype=bool)

_VERTICAL_BOX_SEP = ' '

_VERTICAL_SQUARE_SEP = '|'


class BHBABoard(object):
    """
    Binary 5D hyper-box array for storing a sudoku board.
    """

    def __init__(self):
        self._hyperbox = np.ones(shape=_SHAPE, dtype=bool)

    def __str__(self):
        result = ''
        for _boxrow in range(3):
            for _subrow in range(3):
                # Append three lines
                for _num_div3 in range(3):
                    # Append a single line
                    for _boxcol in range(3):
                        for _subcol in range(3):
                            for _num_mod3 in range(3):
                                _num = 3 * _num_div3 + _num_mod3
                                filled = self._hyperbox[
                                    _boxrow, _subrow, _boxcol, _subcol, _num,
                                ]
                                result += str(_num + 1) if filled else ' '
                            # Append a vertical square separator if needed
                            if _subcol < 2:
                                result += _VERTICAL_SQUARE_SEP
                        # Append a vertical box separator if needed
                        if _boxcol < 2:
                            result += _VERTICAL_BOX_SEP
                    result += '\n'
                # Append a horizontal square separator if needed
                if _subrow < 2:
                    result += _HORIZONTAL_SQUARE_SEP
            # Append a horizontal box separator if needed
            if _boxrow < 2:
                result += _HORIZONTAL_BOX_SEP

        return result

    def insert(self, row, column, number):
        """
        Fill a square with the given number.

        Set the empty square at ``(row, col)`` to ``num``, and remove all
        other candidates from there.

        Parameters
        ----------
        row : int
            Row of the square to fill. One-based indexing.
        column : int
            Column of the square to fill. One-based indexing.
        number : int
            Number to fill the given square with. One-based indexing.

        Raises
        ------
        ValueError
            If the number is not a candidate in the given square.
        """

        # Convert to zero-based indexing
        _row = row - 1
        _col = column - 1
        _num = number - 1

        # Find the 5D coordinates corresponding to the given square and number
        _boxrow, _subrow = self._1d_to_2d(_row)
        _boxcol, _subcol = self._1d_to_2d(_col)

        try:
            self._put(_boxrow, _subrow, _boxcol, _subcol, _num)
        except ValueError:
            msg = "{} is not a candidate in square ({}, {})."
            raise ValueError(msg.format(number, row, column))

    @classmethod
    def from_array(cls, array):
        """
        Instantiate this class from the given 2D array.

        Parameters
        ----------
        array : 2D array of shape (9, 9) of float or None
            2D integer array representing the board. Items are (1-based)
            numbers in the corresponding square, or None if there are
            multiple candidates at that position.

        Returns
        -------
        board : BHBABoard
            The instance created from the given 2D array.
        """
        obj = cls()

        for row, row_squares in enumerate(array, start=1):
            for column, number in enumerate(row_squares, start=1):
                if number is None:
                    continue
                else:
                    obj.insert(row, column, number)

        return obj

    def _1d_to_2d(self, i):
        """
        Convert 1D (linear) coordinate to 2D (bax-based) coordinates.

        Given a single index referring to a row (or column) return the two
        indices corresponding to the box, and subrow (or subcolumn) within
        that boxrow (or boxcolumn).

        Parameters
        ----------
        i : int, 0 to 8
            Row or column index to convert. Zero-based.

        Returns
        -------
        boxidx : int, 0 to 2
            Index of the boxrow/boxcolumn containing the given row/column.
            Zero-based.
        subidx : int, 0 to 2
            Index of the row/column inside the box that contains the given
            row/column. Zero-based.
        """
        return i // 3, i % 3

    def _put(self, _boxrow, _subrow, _boxcol, _subcol, _num):
        """
        Fill a square with the given number.

        Set the empty square at ``(_boxrow, _subrow, _boxcol, _subcol)`` to
        ``_num``, and remove all other candidates from there.

        Parameters
        ----------
        _boxrow : int, 0 to 2
            Boxrow of the square to be filled. Zero-based indexing.
        _subrow : int, 0 to 2
            Subrow of the square to be filled. Zero-based indexing.
        _boxcol : int, 0 to 2
            Boxcolumn of the square to be filled. Zero-based indexing.
        _subcol : int, 0 to 2
            Subcolumn of the square to be filled. Zero-based indexing.
        _num : int, 0 to 8
            Number to fill the given square with. Zero-based indexing.

        Raises
        ------
        ValueError
            If the number is not a candidate in the given square.
        """

        # Raise if the number is not a candidate in the given square
        if not self._hyperbox[_boxrow, _subrow, _boxcol, _subcol, _num]:
            msg = "{} is not a candidate at ({}, {}, {}, {})."
            raise ValueError(
                msg.format(_num, _boxrow, _subrow, _boxcol, _subcol)
            )

        # Remove `num` candidates from its row, column and box
        self._hyperbox[_boxrow, _subrow, :, :, _num] = _TRUE_RECTANGLE
        self._hyperbox[:, :, _boxcol, _subcol, _num] = _TRUE_RECTANGLE
        self._hyperbox[_boxrow, :, _boxcol, :, _num] = _TRUE_RECTANGLE

        # Remove all candidate numbers from its square
        self._hyperbox[_boxrow, _subrow, _boxcol, _subcol, :] = _TRUE_LINE

        # Fill the square with the given candidate
        self._hyperbox[_boxrow, _subrow, _boxcol, _subcol, _num] = True

    def quick_fill(self):
        """
        Fill in some squares with valid (definite) candidates quickly.
        """
        self._quick_fill()

    def _quick_fill(self):
        raise NotImplementedError()
