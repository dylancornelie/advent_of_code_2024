from enum import Enum, auto
import time
from multiprocessing import Pool


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    LEFT = auto()
    DOWN = auto()


file = open("./input.txt", "r")
initial_rows = file.read().split("\n")
offset = len(initial_rows) - 1
iteration_threshold = len(initial_rows) * 4

for x, row in enumerate(initial_rows):
    if "^" in row:
        initial_guard_position = (x, row.index("^"))


def compute_next_arrays(rows):
    next_rights = []
    for row in rows:
        current_nexts = {}
        for y, cell in enumerate(row):
            if cell == "#":
                if current_nexts.keys():
                    most_recent_obstacle = max(current_nexts.keys()) + 2
                else:
                    most_recent_obstacle = 0

                for n in range(most_recent_obstacle, y):
                    current_nexts[n] = y - 1
        next_rights.append(current_nexts)

    next_lefts = []
    for row in rows:
        current_nexts = {}
        for y, cell in enumerate(list(reversed(row))):
            if cell == "#":
                if current_nexts.keys():
                    most_recent_obstacle = offset + 1 - min(current_nexts.keys())
                else:
                    most_recent_obstacle = 0
                for n in range(most_recent_obstacle, y):
                    current_nexts[offset - n] = offset - (y - 1)
        next_lefts.append(current_nexts)
    transposed_rows = transpose_grid(rows)
    next_downs = []
    for row in transposed_rows:
        current_nexts = {}
        for y, cell in enumerate(row):
            if cell == "#":
                if current_nexts.keys():
                    most_recent_obstacle = max(current_nexts.keys()) + 2
                else:
                    most_recent_obstacle = 0

                for n in range(most_recent_obstacle, y):
                    current_nexts[n] = y - 1
        next_downs.append(current_nexts)

    next_ups = []
    for row in transposed_rows:
        current_nexts = {}
        for y, cell in enumerate(list(reversed(row))):
            if cell == "#":
                if current_nexts.keys():
                    most_recent_obstacle = offset + 1 - min(current_nexts.keys())
                else:
                    most_recent_obstacle = 0

                for n in range(most_recent_obstacle, y):
                    current_nexts[offset - n] = offset - (y - 1)
        next_ups.append(current_nexts)
    return next_ups, next_rights, next_downs, next_lefts


def transpose_grid(grid):
    transposed_grid = []
    for x, row in enumerate(grid):
        for y, letter in enumerate(row):
            if x == 0:
                transposed_grid.append([])
            transposed_grid[y].append(letter)

    if isinstance(grid[0], str):
        for i in range(len(transposed_grid)):
            transposed_grid[i] = "".join(transposed_grid[i])
    return transposed_grid


def remember_visited(curr_pos, next_pos, guard_direction, local_rows):
    curr_x, curr_y = curr_pos
    next_x, next_y = next_pos
    if guard_direction == Direction.UP:
        for i in range(next_x, curr_x + 1):
            row_to_edit = list(local_rows[i])
            row_to_edit[curr_y] = "X"
            local_rows[i] = "".join(row_to_edit)
    elif guard_direction == Direction.RIGHT:
        row_to_edit = list(local_rows[curr_x])
        for i in range(curr_y, next_y + 1):
            row_to_edit[i] = "X"
        local_rows[curr_x] = "".join(row_to_edit)
    elif guard_direction == Direction.DOWN:
        for i in range(curr_x, next_x + 1):
            row_to_edit = list(local_rows[i])
            row_to_edit[curr_y] = "X"
            local_rows[i] = "".join(row_to_edit)
    elif guard_direction == Direction.LEFT:
        row_to_edit = list(local_rows[curr_x])
        for i in range(next_y, curr_y + 1):
            row_to_edit[i] = "X"
        local_rows[curr_x] = "".join(row_to_edit)


def simulate_guard_opti(
    next_ups, next_rights, next_downs, next_lefts, rows=None, should_draw=False
) -> bool:
    local_rows = rows or initial_rows.copy()
    guard_position = initial_guard_position
    guard_direction = Direction.UP
    has_reached_outside = False
    iteration = 0
    while not has_reached_outside and iteration < iteration_threshold:
        iteration += 1
        guard_x, guard_y = guard_position
        if guard_direction == Direction.UP:
            next_x = next_ups[guard_y].get(guard_x)
            if next_x is None:
                has_reached_outside = True
                next_x = 0
            next_pos = (next_x, guard_y)
            if should_draw:
                remember_visited(guard_position, next_pos, guard_direction, local_rows)
            guard_position = next_pos
            guard_direction = Direction.RIGHT
        elif guard_direction == Direction.RIGHT:
            next_y = next_rights[guard_x].get(guard_y)
            if next_y is None:
                has_reached_outside = True
                next_y = len(local_rows[0]) - 1
            next_pos = (guard_x, next_y)
            if should_draw:
                remember_visited(guard_position, next_pos, guard_direction, local_rows)
            guard_position = next_pos
            guard_direction = Direction.DOWN
        elif guard_direction == Direction.DOWN:
            next_x = next_downs[guard_y].get(guard_x)
            if next_x is None:
                has_reached_outside = True
                next_x = len(local_rows[0]) - 1
            next_pos = (next_x, guard_y)
            if should_draw:
                remember_visited(guard_position, next_pos, guard_direction, local_rows)
            guard_position = next_pos
            guard_direction = Direction.LEFT
        elif guard_direction == Direction.LEFT:
            next_y = next_lefts[guard_x].get(guard_y)
            if next_y is None:
                has_reached_outside = True
                next_y = 0
            next_pos = (guard_x, next_y)
            if should_draw:
                remember_visited(guard_position, next_pos, guard_direction, local_rows)
            guard_position = next_pos
            guard_direction = Direction.UP
    return has_reached_outside


def simulate_obstacle_for_row(row_index) -> int:
    local_result = 0
    local_initial_rows = initial_rows.copy()
    for y in range(len(local_initial_rows)):
        local_rows = local_initial_rows.copy()
        row_to_modify = list(local_rows[row_index])
        row_to_modify[y] = "#"
        local_rows[row_index] = row_to_modify
        has_reached_outside = simulate_guard_opti(*compute_next_arrays(local_rows))
        if has_reached_outside is False:
            local_result += 1
    return local_result


def main():
    rows = initial_rows.copy()

    def move_guard(next_x, next_y):
        row_as_char_array = list(rows[next_x])
        row_as_char_array[next_y] = "X"
        rows[next_x] = "".join(row_as_char_array)
        return (next_x, next_y)

    def simulate_guard(rows):
        guard_direction = Direction.UP
        guard_position = initial_guard_position
        iteration = 0
        try:
            while iteration < iteration_threshold * len(rows):
                iteration += 1
                if guard_direction == Direction.UP:
                    curr_x, curr_y = guard_position
                    next_x, next_y = curr_x - 1, curr_y
                    if next_x < 0 or next_y < 0:
                        raise IndexError()
                    next_location = rows[next_x][next_y]
                    if next_location == "#":
                        guard_direction = Direction.RIGHT
                    else:
                        guard_position = move_guard(next_x, next_y)
                elif guard_direction == Direction.RIGHT:
                    curr_x, curr_y = guard_position
                    next_x, next_y = curr_x, curr_y + 1
                    if next_x < 0 or next_y < 0:
                        raise IndexError()
                    next_location = rows[next_x][next_y]
                    if next_location == "#":
                        guard_direction = Direction.DOWN
                    else:
                        guard_position = move_guard(next_x, next_y)
                elif guard_direction == Direction.DOWN:
                    curr_x, curr_y = guard_position
                    next_x, next_y = curr_x + 1, curr_y
                    if next_x < 0 or next_y < 0:
                        raise IndexError()
                    next_location = rows[next_x][next_y]
                    if next_location == "#":
                        guard_direction = Direction.LEFT
                    else:
                        guard_position = move_guard(next_x, next_y)
                elif guard_direction == Direction.LEFT:
                    curr_x, curr_y = guard_position
                    next_x, next_y = curr_x, curr_y - 1
                    if next_x < 0 or next_y < 0:
                        raise IndexError()
                    next_location = rows[next_x][next_y]
                    if next_location == "#":
                        guard_direction = Direction.UP
                    else:
                        guard_position = move_guard(next_x, next_y)
        except IndexError:
            pass

    rows = initial_rows.copy()
    start_time = time.time()
    simulate_guard(rows)
    result = 0
    for row in rows:
        result += row.count("X") + row.count("^")
    print(f"Part 1 := {result}")
    print("--- %s seconds ---" % (time.time() - start_time))

    rows = initial_rows.copy()
    start_time = time.time()
    simulate_guard_opti(*compute_next_arrays(rows), rows, True)
    result = 0
    for row in rows:
        result += row.count("X")
    print(f"Part 1 opti := {result}")
    print("--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    result = 0
    for x in range(len(initial_rows)):
        result += simulate_obstacle_for_row(x)

    print(f"Part 2 := {result}")
    # 167.54149413108826 seconds
    # 110.30688691139221 seconds
    print("--- %s seconds ---" % (time.time() - start_time))

    result = 0
    start_time = time.time()
    with Pool(10) as p:
        thread_result = p.map(simulate_obstacle_for_row, range(len(initial_rows)))
    result = sum(thread_result)

    print(f"Part 2 parralel:= {result}")
    # --- 47.452966928482056 seconds ---
    # --- 23.373275995254517 seconds ---
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
