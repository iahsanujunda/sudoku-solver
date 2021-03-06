from utils.utils import *

# Declare units
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
main_diagonal_units = [rows[idx] + cols[idx] for idx in range(0, 9)]
reversed_diagonal_units = [rows[8 - idx] + cols[idx] for idx in range(0, 9)]

# Must be called after all units (including diagonals) are added to the unitlist
unitlist = row_units + column_units + square_units + [main_diagonal_units] + [reversed_diagonal_units]
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if we have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # Populate twins in peers
    twin_boxes = [
        [box_a, box_b]
        for box_a in values
        for box_b in peers[box_a]
        if values[box_a] == values[box_b]
           and len(values[box_a]) == 2
    ]

    for twin_box in twin_boxes:
        box_a_peers = peers[twin_box[0]]
        box_b_peers = peers[twin_box[1]]
        common_intersect = box_a_peers & box_b_peers
        single_peer = [peer for peer in common_intersect if len(values[peer]) > 1]

        for i in single_peer:
            for discard in values[twin_box[0]]:
                values = assign_value(values, i, values[i].replace(discard, ''))
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    found_keys = [k for k in values.keys() if len(values[k]) == 1]
    for key in found_keys:
        for peer in peers[key]:
            values[peer] = values[peer].replace(values[key], '')

    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned
    """
    for unit in unitlist:
        for digit in cols:
            dplaces = [key for key in unit if digit in values[key]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # strategies
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False
    """
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved!

    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Uses recursion to solve each one of the resulting sudokus,
    # and if one returns a value (not False), returns the answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(puzzle_dict):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = search(puzzle_dict)
    return values
