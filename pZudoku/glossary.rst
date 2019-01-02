**Board**
    The square-shaped grid representing a sudoku puzzle. Consists of multiple
    smaller *squares* (usually 9x9=81 of them). Solving a sudoku board consists
    of filling in all empty *squares* with one of the possible *digits* while
    observing the rules concerning uniqueness in each *unit*.

**Box**
    A rectangular (usually 3-by-3) set of *squares* where every possible *digit*
    appears exactly once.

**Candidate**
    The collection of *digits* that are still valid options for a given (empty)
    *square*.

**Clash**
    A hypothetical state of the sudoku *board* when multiple *digits* appear in
    the same *unit*.

**Column**
    A vertical (usually 9-by-1) set of *squares* where every possible *digit*
    appears exactly once.

**Coordinate(s)**
    The two index values specifying a given *square*. For example, the *row*
    and *column* indices.

**Digit**
    The set of numbers (usually 1 to 9) to fill in the *squares* with.

**Peer**
    The collection of *squares* that share a *unit*. Usually every *square*
    has 20 *peers*.

**Row**
    A horizontal (usually 1-by-9) set of *squares* where every possible *digit*
    appears exactly once.

**Square**
    The smallest building block of the sudoku *board*. It can be either empty
    or filled with one of the *digits*.

**Unit**
    The collective noun for *rows*, *columns* and *boxes*. They contain the
    same number of *squares* (usually 9) and must contain every possible
    *digit* exactly once. Every *square* has exactly three *units*.
