from collections import defaultdict

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = [r + c for r in rows for c in cols]
history = {}  # history must be declared here so that it exists in the assign_values scope


def extract_units(unitlist, boxes):
    """Initialize a mapping from box names to the units that the boxes belong to

    Parameters
    ----------
    unitlist(list)
        a list containing "units" (rows, columns, diagonals, etc.) of boxes

    boxes(list)
        a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)

    Returns
    -------
    dict
        a dictionary with a key for each box (string) whose value is a list
        containing the units that the box belongs to (i.e., the "member units")
    """
    # the value for keys that aren't in the dictionary are initialized as an empty list
    units = defaultdict(list)
    for current_box in boxes:
        for unit in unitlist:
            if current_box in unit:
                # defaultdict avoids this raising a KeyError when new keys are added
                units[current_box].append(unit)
    return units


def extract_peers(units, boxes):
    """Initialize a mapping from box names to a list of peer boxes (i.e., a flat list
    of boxes that are in a unit together with the key box)

    Parameters
    ----------
    units(dict)
        a dictionary with a key for each box (string) whose value is a list
        containing the units that the box belongs to (i.e., the "member units")

    boxes(list)
        a list of strings identifying each box on a sudoku board (e.g., "A1", "C7", etc.)

    Returns
    -------
    dict
        a dictionary with a key for each box (string) whose value is a set
        containing all boxes that are peers of the key box (boxes that are in a unit
        together with the key box)
    """
    # the value for keys that aren't in the dictionary are initialized as an empty list
    peers = defaultdict(set)  # set avoids duplicates
    for key_box in boxes:
        for unit in units[key_box]:
            for peer_box in unit:
                if peer_box != key_box:
                    # defaultdict avoids this raising a KeyError when new keys are added
                    peers[key_box].add(peer_box)
    return peers


def assign_value(values, box, value):
    """You must use this function to update your values dictionary if you want to
    try using the provided visualization tool. This function records each assignment
    (in order) for later reconstruction.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    prev = values2grid(values)
    values[box] = value
    if len(value) == 1:
        history[values2grid(values)] = (prev, (box, value))
    return values


def cross(A, B):
    """Cross product of elements in A and elements in B """
    return [x + y for x in A for y in B]


def values2grid(values):
    """Convert the dictionary board representation to as string

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    """
    res = []
    for r in rows:
        for c in cols:
            v = values[r + c]
            res.append(v if len(v) == 1 else '.')
    return ''.join(res)


def grid2values(grid):
    """Convert grid into a dict of {square: char} with '123456789' for empties.

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    Returns
    -------
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
            then the value will be '123456789'.
    """
    assert len(grid) == 81, "Grid must have length of 81"

    sudoku_grid = {}
    for val, key in zip(grid, boxes):
        if val == '.':
            sudoku_grid[key] = '123456789'
        else:
            sudoku_grid[key] = val
    return sudoku_grid


def display(values):
    """Display the values as a 2-D grid.

    Parameters
    ----------
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print()


def reconstruct(values, history) -> list:
    """Returns the solution as a sequence of value assignments 

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    history(dict)
        a dictionary of the form {key: (key, (box, value))} encoding a linked
        list where each element points to the parent and identifies the value
        assignment that connects from the parent to the current state

    Returns
    -------
    list
        a list of (box, value) assignments that can be applied in order to the
        starting Sudoku puzzle to reach the solution
    """
    path = []
    prev = values2grid(values)
    while prev in history:
        prev, step = history[prev]
        path.append(step)
    return path[::-1]


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


def solve(grid):
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
    values = grid2values(grid)
    values = search(values)
    return values
