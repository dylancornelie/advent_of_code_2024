from collections import defaultdict


file = open("./input.txt", "r")
grid = file.read().split("\n")
grid_size = len(grid)
anthenas_group_by_frequency = defaultdict(list)
for index_row, row in enumerate(grid):
    for index_col, cell in enumerate(row):
        if cell != ".":
            anthenas_group_by_frequency[cell].append((index_row, index_col))

antinodes = set()

for frequency, anthenas in anthenas_group_by_frequency.items():
    for current_anthena in anthenas:
        curr_row, curr_col = current_anthena
        for anthena in anthenas_group_by_frequency[frequency]:
            if anthena == current_anthena:
                continue
            anthena_row, anthena_col = anthena
            (vec_row, vec_col) = (curr_row - anthena_row, curr_col - anthena_col)
            front_antinode = (curr_row + vec_row, curr_col + vec_col)
            # Check if front_antinode not out of bound
            if all(map(lambda pos: pos >= 0 and pos < grid_size, front_antinode)):
                antinodes.add(front_antinode)
            back_antinode = (curr_row - 2 * vec_row, curr_col - 2 * vec_col)
            # Check if back_antinode not out of bound
            if all(map(lambda pos: pos >= 0 and pos < grid_size, back_antinode)):
                antinodes.add(back_antinode)

print("Part 1 := %s" % len(antinodes))


def vector_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def vector_minus(a, b):
    return (a[0] - b[0], a[1] - b[1])


def check_vector_inbound(vector):
    return all(map(lambda pos: pos >= 0 and pos < grid_size, vector))


antinodes.clear()
for frequency, anthenas in anthenas_group_by_frequency.items():
    for current_anthena in anthenas:
        curr_row, curr_col = current_anthena
        for anthena in anthenas_group_by_frequency[frequency]:
            if anthena == current_anthena:
                continue
            anthena_row, anthena_col = anthena
            (vec_row, vec_col) = (curr_row - anthena_row, curr_col - anthena_col)
            front_antinode = (curr_row + vec_row, curr_col + vec_col)
            while check_vector_inbound(front_antinode):
                antinodes.add(front_antinode)
                front_antinode = vector_add(front_antinode, (vec_row, vec_col))
            back_antinode = (curr_row - vec_row, curr_col - vec_col)
            # Check if back_antinode not out of bound
            while check_vector_inbound(back_antinode):
                antinodes.add(back_antinode)
                back_antinode = vector_minus(back_antinode, (vec_row, vec_col))


print("Part 2 := %s" % len(antinodes))
