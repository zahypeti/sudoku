def _boxrows(row, box_height):
    """
    Return a slice that corresponds to the rows of the box containing the given
    single row.
    """
    start = row // box_height * box_height
    finish = start + box_height
    return slice(start, finish)


def _boxcols(col, box_width):
    """
    Return a slice that corresponds to the columns of the box containing the
    given single column.
    """
    start = col // box_width * box_width
    finish = start + box_width
    return slice(start, finish)


def boxindex(row, col, box_height, box_width):
    """
    Return the index of the box containing the given square. rowcol2box
    """
    return (row // box_height * box_height) + (col // box_width)


def rows_cols(*args):
    """
    Return a 2-tuple of slices corresponding to rows and columns containing
    the given box / square.

    Usages
    ------
    row_slice, col_slice = rows_cols(box, box_height, box_width)
    row_slice, col_slice = rows_cols(row, col, box_height, box_width)

    """
    if len(args) == 3:
        box, box_height, box_width = args
        # Get the row and column in the given box with lowest index
        row = box // box_height
        col = (box % box_height) * box_width
    elif len(args) == 4:
        row, col, box_height, box_width = args
    else:
        raise ValueError

    row_slice = _boxrows(row, box_height)
    col_slice = _boxcols(col, box_width)
    return row_slice, col_slice


def square(box_id, position, box_height, box_width):
    """
    row, col = square(box, pos)
    """
    row = (box_id // box_height) * box_height + position // box_width
    col = (box_id % box_height) * box_height + (position % box_width)
    return row, col
