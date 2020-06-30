import random
import string
import sys

from utils.utils import *
from objects.Board import Board

# Declare units

if __name__ == "__main__":
    sudoku_puzzle = ''

    if len(sys.argv) == 2:
        sudoku_puzzle = str(sys.argv[1])
    else:
        puzzle_choice = [
            '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3',
            '.7.......6.......195...............4.............8.....2....9.................6..',
            '....8.....1..4.....57...6..3............2..1.......43.........8.........9.1.....4',
            '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        ]

        sudoku_puzzle = puzzle_choice[3]  # random.randrange(2)

    board = Board(sudoku_puzzle)
    board.display_board()

    # run agent
    result = solve(sudoku_puzzle)

    # update and display solved board
    board.update_board_with_dict(result)
    board.display_board()

    try:
        import PySudoku

        PySudoku.play(grid2values(sudoku_puzzle), result, history)
    except ImportError:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
    except SystemExit:
        pass
