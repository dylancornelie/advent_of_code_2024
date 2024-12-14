import functools
from math import log10

file = open("./input.txt", "r").read()
input = list(map(lambda x: int(x), file.split(" ")))


def get_number_of_digits(x):
    return int(log10(x)) + 1


def split_number_in_two(x):
    number_of_digits = get_number_of_digits(x)
    assert number_of_digits % 2 == 0
    return divmod(x, pow(10, number_of_digits / 2))


@functools.cache
def simulate_stone(stone, depth=75):
    if depth == 0:
        return 1
    if stone == 0:
        return simulate_stone(1, depth - 1)
    if get_number_of_digits(stone) % 2 == 0:
        return sum(
            map(lambda s: simulate_stone(s, depth - 1), split_number_in_two(stone))
        )
    return simulate_stone(stone * 2024, depth - 1)


stone_arrangement = input[:]
print(sum([simulate_stone(x) for x in stone_arrangement]))
