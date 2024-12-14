from collections import defaultdict
import re
import sys

sys.setrecursionlimit(10**6)

file = open("./input.txt", "r")
inputs = file.read().split("\n")

len_x = 101
len_y = 103

# len_x = 11
# len_y = 7

middle_horizontal_pos = len_y // 2
middle_vertical_pos = len_x // 2


def is_christmas_tree(final_positions):
    for y in range(len_y):
        res = list(filter(lambda key: key[1] == y, final_positions.keys()))
        if len(res) != (y + 1) * 2:
            return False
    return True


def move_guard(pos, speed):
    x, y = pos[0] + speed[0], pos[1] + speed[1]
    if x >= len_x:
        x = x - len_x
    elif x < 0:
        x = len_x + x

    if y >= len_y:
        y = y - len_y
    elif y < 0:
        y = len_y + y

    return (x, y)


def simulate_guard(start_pos, speed, remaining_simulation):
    if remaining_simulation == 0:
        return start_pos
    else:
        new_pos = move_guard(start_pos, speed)
        return simulate_guard(new_pos, speed, remaining_simulation - 1)


def print_map():
    for y in range(len_y):
        row = ""
        for x in range(len_x):
            if (
                (x, y) in key_to_ignore
                or y == middle_horizontal_pos
                or x == middle_vertical_pos
            ):
                row += "#"
            elif final_positions.get((x, y), None) is not None:
                row += str(final_positions[(x, y)])
            else:
                row += "."
        print(row)


def simulate_guard_for_n_seconds(pos, speed, seconds):
    return (
        (pos[0] + speed[0] * seconds) % len_x,
        (pos[1] + speed[1] * seconds) % len_y,
    )


def simulate_n_blinks(n):
    final_positions = {}
    for input in inputs:
        px, py, vx, vy = [int(x) for x in re.findall("-?\d+", input)]
        final_position = simulate_guard((px, py), (vx, vy), n)
        if final_positions.get(final_position):
            final_positions[final_position] += 1
        else:
            final_positions[final_position] = 1
    return final_positions


final_positions = simulate_n_blinks(100)
key_to_ignore = set()
for key in final_positions.keys():
    x, y = key
    if y == middle_horizontal_pos or x == middle_vertical_pos:
        key_to_ignore.add(key)

top_left = 0
top_right = 0
bottom_left = 0
bottom_right = 0

for coord, number_of_robot in final_positions.items():
    if coord in key_to_ignore:
        continue
    x, y = coord
    if x < middle_vertical_pos and y < middle_horizontal_pos:
        top_left += number_of_robot
    elif x > middle_vertical_pos and y < middle_horizontal_pos:
        top_right += number_of_robot
    elif x > middle_vertical_pos and y > middle_horizontal_pos:
        bottom_right += number_of_robot
    elif x < middle_vertical_pos and y > middle_horizontal_pos:
        bottom_left += number_of_robot

print("Result part 1 := %s" % (top_left * top_right * bottom_left * bottom_right))


for seconds in range (10**6):
    seen_robots = set()
    for input in inputs:
        px, py, vx, vy = [int(x) for x in re.findall("-?\d+", input)]
        final_position = simulate_guard_for_n_seconds((px, py), (vx, vy), seconds)
        seen_robots.add(final_position)
    # No overlap between robots
    if len(seen_robots) == len(inputs):
        print(seconds)
        final_positions.clear()
        for pos in seen_robots:
            final_positions[pos] = 1
        print_map()
        break
