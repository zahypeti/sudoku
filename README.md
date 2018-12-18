[
  ![CirrusCI](https://api.cirrus-ci.com/github/pzahemszky/sudoku.svg)
](https://cirrus-ci.com/github/pzahemszky/sudoku)

# sudoku

A Python implementation of a sudoku solver, using my own 6D boolean array data structure as well as my `_quick_fill` and recursion strategies.

## Usage

### Store the squares in a list of lists
```python
>>> squares = [
...         [4, 0, 0, 0, 0, 0, 8, 0, 5],
...         [0, 3, 0, 0, 0, 0, 0, 0, 0],
...         [0, 0, 0, 7, 0, 0, 0, 0, 0],
...         [0, 2, 0, 0, 0, 0, 0, 6, 0],
...         [0, 0, 0, 0, 8, 0, 4, 0, 0],
...         [0, 0, 0, 0, 1, 0, 0, 0, 0],
...         [0, 0, 0, 6, 0, 3, 0, 7, 0],
...         [5, 0, 0, 2, 0, 0, 0, 0, 0],
...         [1, 0, 4, 0, 0, 0, 0, 0, 0],
...     ]
```

### Create a `Board` instance from `squares`

[//]: # (Note: keep this tested in tests.test_api)

```python
>>> from sudoku.api import Board
>>> my_board = Board.from_array(squares)
```

### Solve!

[//]: # (Note: keep this tested in tests.test_api)

```
>>> my_board.solve()
>>> print(my_board)
4 1 7 | 3 6 9 | 8 2 5
6 3 2 | 1 5 8 | 9 4 7
9 5 8 | 7 2 4 | 3 1 6
---------------------
8 2 5 | 4 3 7 | 1 6 9
7 9 1 | 5 8 6 | 4 3 2
3 4 6 | 9 1 2 | 7 5 8
---------------------
2 8 9 | 6 4 3 | 5 7 1
5 7 3 | 2 9 1 | 6 8 4
1 6 4 | 8 7 5 | 2 9 3
```
