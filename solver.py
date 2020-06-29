import random
import string
import sys

from utils.utils import *

# Declare units

if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    if len(sys.argv) == 2:
        diag_sudoku_grid = str(sys.argv[1])
    else:
        diag_sudoku_grid = ''.join(random.choice(string.digits) for _ in range(81))

    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku

        PySudoku.play(grid2values(diag_sudoku_grid), result, history)
    except ImportError:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
    except SystemExit:
        pass
