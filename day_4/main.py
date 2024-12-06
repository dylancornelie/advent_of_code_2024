import re

file = open("./input.txt", "r")
grid = file.read().split("\n")

xmas_count = 0
# Horizontal XMAS
for row in grid:
    matches = re.findall("(?=(XMAS|SAMX))", row)
    xmas_count += len(matches)
print(f"horizontal := {xmas_count}")
transpose_grid = []

# A B
# C D
#
# A C
# B D
for row_index, row in enumerate(grid):
    for column_index, letter in enumerate(row):
        if row_index == 0:
            transpose_grid.append([])
        transpose_grid[column_index].append(letter)

for i in range(len(transpose_grid)):
    transpose_grid[i] = "".join(transpose_grid[i])

# Vertical XMAS
for row in transpose_grid:
    matches = re.findall("(?=(XMAS|SAMX))", row)
    xmas_count += len(matches)
print(f"vertical :={xmas_count}")


# A B C D
# E F G H
# I J K L
# M N O P
#
# A (0, 0)
# B E (0, 1) + (1, 0)
# C F I (0, 2) + (1, 1) + (2, 0)
# D G J M (0, 3) + (1, 2) + (2, 1) + (3, 0)


# H K N
# L O
# P
# Transpose the array diagonnaly
def transpose_grid_diagonnaly(grid):
    result_left = []
    result_right = []
    for x in range(len(grid)):
        y = 0
        left_part = []
        right_part = []
        while x >= 0:
            left_part.append(grid[y][x])
            right_part.append(list(reversed(list(reversed(grid))[y]))[x])
            y += 1
            x -= 1

        result_left.append(left_part)
        result_right.append(right_part)
    result = result_left.copy()
    result_right.pop()
    result.extend(list(reversed(result_right)))
    return result


diagonals = transpose_grid_diagonnaly(grid)
diagonals.extend(transpose_grid_diagonnaly(list(reversed(grid))))
for row in diagonals:
    matches = re.findall("(?=(XMAS|SAMX))", "".join(row))
    xmas_count += len(matches)
print(f"diagonal := {xmas_count}")


xmas_count = 0


# Traverse the grid row by row
def is_xmas_shape(x, y, grid):
    # Check if the middle part is an A
    try:
        middle = grid[x + 1][y + 1]
        if middle != "A":
            return False
        top_left = grid[x][y]
        top_right = grid[x][y + 2]
        bottom_left = grid[x + 2][y]
        bottom_right = grid[x + 2][y + 2]
        expected_letters = ["M", "S"]
        if (
            top_left not in expected_letters
            or top_right not in expected_letters
            or bottom_left not in expected_letters
            or bottom_right not in expected_letters
        ):
            return False
        first_diag = top_left + middle + bottom_right
        second_diag = top_right + middle + bottom_left
        first_diag_match = re.match('MAS|SAM', first_diag)
        second_diag_match = re.match('MAS|SAM', second_diag)
        if not first_diag_match or not second_diag_match:
            return False
        return True
    except IndexError:
        return False


# Iterate over each grid element
for x, row in enumerate(grid):
    for y, letter in enumerate(row):
        if is_xmas_shape(x, y, grid):
            xmas_count += 1
print(xmas_count)
