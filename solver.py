import random
import string
import sys

from utils import agent
from utils.utils import history
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

        sudoku_puzzle = puzzle_choice[random.randrange(4)]  # random.randrange(2)

    board = Board(sudoku_puzzle)
    board.display_board()

    # run agent
    result = agent.solve(board.get_puzzle_dict())

    # update and display solved board
    board.update_board_with_dict(result)
    board.display_board()

    try:
        import PySudoku

        play_board = Board(sudoku_puzzle)

        PySudoku.play(play_board.get_puzzle_dict(), result, history)
    except ImportError:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
    except SystemExit:
        pass
