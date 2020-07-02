import random
import string
import sys

from utils import agent
from utils.utils import history
from utils.puzzles import puzzle_choices
from objects.Board import Board

# Declare units

if __name__ == "__main__":
    sudoku_puzzle = ''

    if len(sys.argv) == 2:
        sudoku_puzzle = str(sys.argv[1])
    else:
        sudoku_puzzle = puzzle_choices[random.randrange(6)]  # random.randrange(4)

    board = Board(sudoku_puzzle)
    board.display_board()

    # run agent
    solution = agent.solve(board.get_puzzle_dict())
    if not solution:
        sys.exit('Invalid diagonal puzzle!')

    # update and display solved board
    board.update_board_with_dict(solution)
    board.display_board()

    try:
        import PySudoku

        play_board = Board(sudoku_puzzle)

        PySudoku.play(play_board.get_puzzle_dict(), solution, history)
    except ImportError:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
    except SystemExit:
        pass
