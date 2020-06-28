# AI Technique to solve Sudoku

<p style="text-align:center;">
<img src="./images/sudoku.png" height="400" width="350" alt="sudoku-solver" />
<img src="./images/solved.png" height="400" width="350" alt="sudoku-solver" />
</p>

In this project, we developed Sudoku-solving agent to solve [_diagonal sudoku puzzles_](https://sudoku.cool/x-sudoku.php) and implement a constraint strategy called "naked twins". A diagonal Sudoku puzzle is identical to traditional Sudoku puzzles with the added constraint that the boxes on the two main diagonals of the board must also contain the digits 1-9 in each cell (just like the rows, columns, and 3x3 blocks).

The naked twins strategy says that if we have two or more unallocated boxes in a unit and there are only two digits that can go in those two boxes, then those two digits can be eliminated from the possible assignments of all other boxes in the same unit.

## Techniques

- Constraint Propagation
- Depth-first Search Algorithm

## Quickstart Guide

Everything needed to run this project has been exported as conda environment. Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) according to your system, once it is installed, import the enviroment from `environment.yml` file.

```bash
conda env create -f environment.yml     # import the conda environment
conda activate aind                     # activates the environment
```

Before running the agent, make sure that all checks are passed by running the test suite.

```bash
python -m unittest -v
```

If all checks are clear, the agent can be run from the CLI using the following command

```bash
python solution.py
```

## Strategy Guide




## Submission

To submit your code, run `udacity submit` from a terminal in the top-level directory of this project. You will be prompted for a username and password the first time the script is run. If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

The Udacity-PA CLI tool is automatically installed with the AIND conda environment provided in the classroom, but you can also install it manually by running `pip install udacity-pa`. You can submit your code for scoring by running `udacity submit`. The project assistant server has a collection of unit tests that it will execute on your code, and it will provide feedback on any successes or failures. You must pass all test cases in the project assistant to pass the project.

Once your project passes all test cases on the Project Assistant, submit the zip file created by the `udacity submit` command in the classroom to automatically receive credit for the project. NOTE: You will not receive personalized feedback for this project on submissions that pass all test cases, however, all other projects in the term do provide personalized feedback on both passing & failing submissions.


## Visualization

**Note:** The `pygame` library is required to visualize your solution -- however, the `pygame` module can be troublesome to install and configure. It should be installed by default with the AIND conda environment, but it is not reliable across all operating systems or versions. Please refer to the pygame documentation [here](http://www.pygame.org/download.shtml), or discuss among your peers in the slack group if you need help.

Running `python solution.py` will automatically attempt to visualize your solution, but you mustuse the provided `assign_value` function (defined in `utils.py`) to track the puzzle solution progress for reconstruction during visuzalization.
