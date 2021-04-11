# AI Technique to solve Sudoku

<p style="text-align:center;">
<img src="./images/sudoku.png" height="400" width="350" alt="sudoku-solver" />
<img src="./images/solved.png" height="400" width="350" alt="sudoku-solver" />
</p>

In this project, we developed Sudoku-solving agent to solve [_diagonal sudoku puzzles_](https://sudoku.cool/x-sudoku.php) and implement a constraint strategy called [naked twins](./pseudocode.md). A diagonal Sudoku puzzle is identical to traditional Sudoku puzzles with the added constraint that the boxes on the two main diagonals of the board must also contain the digits 1-9 in each cell (just like the rows, columns, and 3x3 blocks).

The naked twins strategy says that if we have two or more unallocated boxes in a unit and there are only two digits that can go in those two boxes, then those two digits can be eliminated from the possible assignments of all other boxes in the same unit.

## Techniques

- Constraint Propagation
- Depth-first Search Algorithm

## Quickstart Guide

Everything needed to run this project has been exported as conda environment. Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) according to your system, once it is installed, import the enviroment from `environment.yml` file.

```bash
conda env create -f environment.yml     # import the conda environment
conda activate sudoku                   # activates it
```

Before running the agent, make sure that all checks passed by running the test suite.

```bash
python -m unittest -v
```

If all checks are clear, the agent can be run from the CLI using the following command

```bash
python solver.py
```

### Running custom board puzzle

We can create our own puzzle to be run by this agent. This program accepts optional argument for building custom puzzle. Note that without this argument, the program will pick one of predefined board puzzle at random.

```bash
usage: solver.py [options] puzzle_board
  options:
    puzzle_board    a string representing a sudoku grid. Must be 81 characters long.
                    Ex. '.14.....5......2.........7..........3...4...7...6..4...4....8...........7.......3'
``` 

## Strategy Guide

### 1. Constraint Propagation

We use several contraints to solve this puzzle,

- **elimination contraint**

> When a box has been assigned a digit, then all peers of this box can't have the same digit.

- **only choice constraint**

> When only one box in a unit allows a certain digit, then that box must be assigned that digit.

- **naked twins contraint**

> When two or more unallocated boxes in a unit has the same two digit option that can be assigned to them, then these two digits can be eliminated from the assignment of all other boxes in the same unit

### 2. Depth-first search

![depth-first](https://upload.wikimedia.org/wikipedia/commons/7/7f/Depth-First-Search.gif)

[Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search) is an algorithm to traverse a tree. In our case, the tree represent the possible solutions to solve our sudoku puzzle. Using depth-first, upon encounter with multiple possible solutions, we are going to traverse the first 'branch' we find until exhaustion, i.e. either we find correct solution or all possible constraints are violated. Upon contraint violation, we switch to second available branch and also traverse this branch until exhaustion. The agent will stop on finding the first 'edge' with a solution.

One adversary to depth-first search is breadth-first search, where in case of multiple possible solutions, we are going to take one step into each branch we encounter until a solution is found.

## Visualization

**Note:** The `pygame` library is required to run visualization -- we have include it with the `sudoku` environment, however, the `pygame` module can be troublesome to install and configure, and it is not reliable across all operating systems and versions. Please refer to the pygame documentation [here](http://www.pygame.org/download.shtml) to troubleshoot pygame.

When all requirement of pygame is met, running `python solver.py` will automatically attempt to visualize our solution. Otherwise, the agent will run without visualization.
