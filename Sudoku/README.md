Sudoku Solver

A Python implementation of a Sudoku solver using constraint satisfaction techniques including backtracking and AC-3 (Arc Consistency 3) algorithm for improved performance.
Overview
This program solves 9x9 Sudoku puzzles by combining two powerful algorithmic approaches:

AC-3 Constraint Propagation: Reduces the search space by enforcing arc consistency
Backtracking Search: Systematically explores possible solutions

The solver first applies AC-3 to prune impossible values from each cell's domain, then uses backtracking to find the complete solution.
Features

AC-3 Algorithm: Implements arc consistency to reduce domain sizes before search
Backtracking Search: Efficient recursive solution finding with constraint checking
Constraint Validation: Checks row, column, and 3x3 box constraints
Domain Management: Tracks possible values for each empty cell
Input Flexibility: Reads puzzles from standard input
Solution Validation: Includes validator function to verify correctness

Algorithm Details
AC-3 (Arc Consistency 3)

Purpose: Reduces domain sizes by enforcing local consistency
Process: Iteratively removes values that cannot satisfy binary constraints
Benefits: Significantly reduces search space for backtracking
Implementation: Uses queue-based approach with constraint propagation

Backtracking Search

Strategy: Depth-first search with constraint checking
Pruning: Only explores valid moves that satisfy Sudoku rules
Efficiency: Combined with AC-3 preprocessing for optimal performance

Constraint System
The solver recognizes three types of constraints:

Row Constraints: No duplicate numbers in any row
Column Constraints: No duplicate numbers in any column
Box Constraints: No duplicate numbers in any 3x3 subgrid

Requirements
python 3.x
numpy
Installation
bashpip install numpy
Usage
Input Format
The program expects a 9x9 Sudoku grid via standard input, with:

Numbers 1-9 for filled cells
0 for empty cells
Space-separated values
One row per line

Example Input File (puzzle.txt)
5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9
Running the Solver
bashpython sudoku_solver.py < puzzle.txt
Expected Output
[5 3 4 6 7 8 9 1 2]
[6 7 2 1 9 5 3 4 8]
[1 9 8 3 4 2 5 6 7]
[8 5 9 7 6 1 4 2 3]
[4 2 6 8 5 3 7 9 1]
[7 1 3 9 2 4 8 5 6]
[9 6 1 5 3 7 2 8 4]
[2 8 7 4 1 9 6 3 5]
[3 4 5 2 8 6 1 7 9]
Code Structure
Core Functions
isValid(sudoku_grid, cur_row, cur_col, num)

Checks if placing a number at given position violates Sudoku constraints
Validates row, column, and 3x3 box constraints
Returns True if placement is valid

naiveBackTrack(sudoku_grid, cur_row, cur_col)

Recursive backtracking algorithm
Tries numbers 1-9 for each empty cell
Backtracks when no valid number can be placed

AC3(sudoku_grid)

Implements Arc Consistency 3 algorithm
Reduces domains by enforcing binary constraints
Returns updated domains or False if inconsistent

get_all_constraints()

Generates all binary constraints for the Sudoku puzzle
Creates constraint pairs for rows, columns, and boxes
Returns set of constraint tuples

get_all_domains(sudoku_grid)

Initializes domain sets for each cell
Empty cells get domain {1,2,3,4,5,6,7,8,9}
Filled cells get singleton domain with their value

Helper Functions
arc_reduce(domains, xi, xj)

Reduces domain of variable xi with respect to xj
Removes values that cannot satisfy the constraint
Returns True if domain was modified

neighbors(cell)

Returns all cells that share constraints with given cell
Includes same row, column, and 3x3 box neighbors

validator(sudoku_grid)

Validates a completed Sudoku solution
Checks all constraints are satisfied
Used for solution verification

Performance Characteristics
Time Complexity

AC-3: O(cd³) where c is constraints, d is domain size
Backtracking: O(9^m) where m is empty cells (worst case)
Combined: Significantly better than naive backtracking alone

Space Complexity

Domain Storage: O(81 × 9) = O(729) for maximum domains
Constraint Storage: O(810) for all binary constraints
Recursion Stack: O(81) maximum depth

Algorithm Advantages

AC-3 Preprocessing: Dramatically reduces search space
Early Constraint Checking: Prevents invalid partial solutions
Domain Pruning: Eliminates impossible values early
Systematic Search: Guarantees finding solution if one exists

Testing
The solver can handle:

Easy puzzles (solved mostly by AC-3)
Medium puzzles (require limited backtracking)
Hard puzzles (extensive backtracking needed)
Invalid puzzles (detects unsolvable cases)

Sample Test Cases
bash# Easy puzzle
echo "5 3 4 6 7 8 9 1 2..." | python sudoku_solver.py

# Hard puzzle with multiple empty cells
echo "0 0 0 0 0 0 0 0 0..." | python sudoku_solver.py
Extensions and Improvements
Possible enhancements:

MRV Heuristic: Choose variable with minimum remaining values
Degree Heuristic: Choose variable involved in most constraints
Least Constraining Value: Order values to preserve options
Forward Checking: Immediate constraint propagation after assignment
MAC (Maintaining Arc Consistency): Continuous arc consistency during search
