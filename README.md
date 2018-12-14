|CircleCI|_

.. |CirrusCI| image:: https://api.cirrus-ci.com/github/pzahemszky/sudoku.svg
.. _CirrusCI: https://cirrus-ci.com/github/pzahemszky/sudoku

# sudoku

A Python implementation of a sudoku solver, using my own 3D `bool` data structure as well as my `quick_fill` & recursion strategies.

## Usage

### Create an empty sudoku board
`>>> my_9x9_board = Board()`

### Fill in some squares with the given values
`>>> digits = ('4.....8.5.3..........7......2.....6.....8.4......1.......6.3
.7.5..2.....1.4......')`

`>>> my_9x9_board.from_str(digits)`

### Solve!
`>>> my_9x9_board.solve()`

`>>> print(my_9x9_board)`
