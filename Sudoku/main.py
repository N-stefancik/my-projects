
import itertools
import numpy as np
import sys

cur_row = 0
cur_col = 0

def isValid(sudoku_grid, cur_row, cur_col, num):
  # This method checks if a number inserting in a given
  # number into the spot (cur_row, cur_col) is a valid move
  for i in range(9):
    if(sudoku_grid[cur_row][i] == num):
      return False
  for i in range(9):
    if(sudoku_grid[i][cur_col] == num):
      return False
  start_row = cur_row - cur_row % 3
  start_col = cur_col - cur_col % 3
  for i in range(3):
      for j in range(3):
          if sudoku_grid[start_row + i][start_col + j] == num:
              return False
  return True

def validator(sudoku_grid):
  for row in range(9):
    for col in range(9):
      if isValid(sudoku_grid, row, col, sudoku_grid[row][col]):
        return False
  return True


def naiveBackTrack(sudoku_grid, cur_row, cur_col):
    if cur_col == 9:
        cur_row += 1
        cur_col = 0
    if cur_row == 9:
        return True
    if sudoku_grid[cur_row][cur_col] != 0:
        return naiveBackTrack(sudoku_grid, cur_row, cur_col + 1)
    else:
      for num in range(1, 10):
        if isValid(sudoku_grid, cur_row, cur_col, num):
          sudoku_grid[cur_row][cur_col] = num
          if naiveBackTrack(sudoku_grid, cur_row, cur_col + 1):
              return True
          sudoku_grid[cur_row][cur_col] = 0
    return False

def get_all_constraints():
  constraints = set()
  for row in range(9):
      for col1, col2 in itertools.combinations(range(9), 2):
          constraints.add(((row, col1), (row, col2)))
    # Columns constraints
  for col in range(9):
      for row1, row2 in itertools.combinations(range(9), 2):
          constraints.add(((row1, col), (row2, col)))

  for subgrid_row in range(3):
    for subgrid_col in range(3):
      cells = []
      for i in range(3):
          for j in range(3):
            cells.append((subgrid_row * 3 + i, subgrid_col * 3 + j))
      for (r1, c1), (r2, c2) in itertools.combinations(cells, 2):
        constraints.add(((r1, c1), (r2, c2)))

  return constraints

def get_all_domains(sudoku_grid):
  domains = {}
  for row in range(9):
    for col in range(9):
      if sudoku_grid[row][col] == 0:
        domains[row, col] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
      else:
        domains[(row, col)] = {sudoku_grid[row][col]}
  return domains


def AC3(sudoku_grid, ):
  constraints = get_all_constraints().copy()
  domains = get_all_domains(sudoku_grid)
  queue = list(constraints)
  while queue:
    (xi, xj) = queue.pop(0)
    if arc_reduce(domains, xi, xj):
      if len(domains[xi]) == 0:
        return False
      for xk in neighbors(xi):
        if xk != xj:
          queue.append((xk, xi))
  return domains

def arc_reduce(domains, xi, xj):
  revised = False
  to_remove = set()

  for x in domains[xi]:
    if not any(x != y for y in domains[xj]):
      to_remove.add(x)

  if to_remove:
    domains[xi] -= to_remove
    revised = True

  return revised

  
def neighbors(cell):
    row, col = cell
    neighbors = set()

    # Row and column neighbors
    for i in range(9):
        if i != col:
            neighbors.add((row, i))
        if i != row:
            neighbors.add((i, col))

    # Box neighbors
    box_row, box_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            r, c = box_row + i, box_col + j
            if (r, c) != (row, col):
                neighbors.add((r, c))

    return neighbors
'''
sudoku_grid_naive = sudoku_grid.copy()
if naiveBackTrack(sudoku_grid_naive, 0, 0):
    for row in sudoku_grid_naive:
      print(row)
else:
    print("No solution exists.")
print(validator(sudoku_grid_naive))

sudoku_grid_speedy = sudoku_grid.copy()
# Print original domains
print("Original domains:")
original_domains = get_all_domains(sudoku_grid_speedy)
for key, val in original_domains.items():
    print(f"{key}: {val}")

# Apply AC3
updated_domains = AC3(sudoku_grid_speedy)

# Print updated domains after AC3
print("\nDomains after AC3:")
for key, val in updated_domains.items():
    print(f"{key}: {val}")

if naiveBackTrack(sudoku_grid_speedy, 0, 0):
    for row in sudoku_grid_speedy:
      print(row)
else:
    print("No solution exists.")
print(validator(sudoku_grid_speedy))
'''

sudoku_grid = np.array([list(map(int, line.split())) for line in sys.stdin])

updated_domains = AC3(sudoku_grid)

if naiveBackTrack(sudoku_grid, 0, 0):
    for row in sudoku_grid:
      print(row)
else:
    print("No solution.")