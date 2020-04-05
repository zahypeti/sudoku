Ubuntu:
[
  ![Travis CI build status](https://travis-ci.com/pzahemszky/pZudoku.svg?branch=master)
](https://travis-ci.com/pzahemszky/pZudoku)

[
  ![codecov percentage](https://codecov.io/gh/pzahemszky/pZudoku/branch/master/graph/badge.svg)
](https://codecov.io/gh/pzahemszky/pZudoku)

# pZudoku

A Python 3 implementation of a sudoku solver, using my own 6D boolean array data structure as well as my `_quick_fill` and recursion strategies.

## Prerequisites

You'll need Python 3 installed (3.4 or later), as well as the following
packages.
- `pip >= 9.0.0`
- `setuptools >= 38.6.0`
- `numpy >= 1.15.0`

[//]: # (Note: keep these in sync with setup.py's install_requires)

## Install

- Clone or download the repository from GitHub (e.g. `git clone https://github.com/pzahemszky/pZudoku.git`).
- Change to the `pZudoku` directory (e.g. `cd pZudoku`).
- Install the `pZudoku` Python package (e.g. `pip install --user .`).

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
>>> from pZudoku.api import Board
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

## Uninstall

Remove the `pZudoku` Python package (e.g. `pip uninstall pZudoku`).
