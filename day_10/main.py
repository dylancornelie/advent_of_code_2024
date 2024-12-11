from functools import reduce

file = open("./input.txt", "r").read()
input = file.split("\n")

trail_map = [list(map(lambda y: int(y), x)) for x in input]


def print_trail_map():
    print("\n")
    for x in trail_map:
        print(x)
    print("\n")


def get_valid_adjacent_positions(position, height):
    row, col = position
    adjacent_pos = [(row, col + 1), (row, col - 1), (row + 1, col), (row - 1, col)]

    def filter_out_invalid_pos(position):
        row, col = position
        if row not in range(len(trail_map)) or col not in range(len(trail_map)):
            return False
        if trail_map[row][col] != height + 1:
            return False
        return True

    return list(filter(filter_out_invalid_pos, adjacent_pos))


def travel_to_height_9(position):
    seen_height_9_distinct = set()
    seen_height_9 = list()
    row, col = position
    current_height = trail_map[row][col]
    if current_height == 9:
        seen_height_9_distinct.add(position)
        seen_height_9.append(position)
        return seen_height_9_distinct, seen_height_9
    adjacents = get_valid_adjacent_positions(position, current_height)

    def reduce_travel_to_height_result(acc, pos_adj):
        acc_seen_distinct, acc_seen_all = acc
        result_distinct, result_all = travel_to_height_9(pos_adj)
        acc_seen_distinct.update(result_distinct)
        acc_seen_all.extend(result_all)
        return acc_seen_distinct, acc_seen_all

    if len(adjacents) != 0:
        return reduce(
            reduce_travel_to_height_result,
            adjacents,
            (seen_height_9_distinct, seen_height_9),
        )
    else:
        return seen_height_9_distinct, seen_height_9


possible_starting_points = set()
for row in range(len(trail_map)):
    for col in range(len(trail_map)):
        if trail_map[row][col] == 0:
            possible_starting_points.add((row, col))

score_part1 = 0
score_part2 = 0
for starting_pos in possible_starting_points:
    seen_height_9_distinct, seen_height_9 = travel_to_height_9(starting_pos)
    score_part1 += len(seen_height_9_distinct)
    score_part2 += len(seen_height_9)

print("Part 1 := %s" % score_part1)
print("Part 2 := %s" % score_part2)
