from math import log10

file = open("./input.txt", "r")
initial_rows = file.read().split("\n")
equations = []
for initial_row in initial_rows:
    expected_result, operands = initial_row.split(": ")
    equations.append(
        (int(expected_result), list(map(lambda x: int(x), operands.split(" "))))
    )


def digits(n):
    return int(log10(n)) + 1


def endswith(a, b):
    return (a - b) % 10 ** digits(b) == 0


def is_solvable(expected: int, operands: list[int]) -> bool:
    if len(operands) == 1:
        return expected == operands[0]
    current_operand = operands[-1]
    if expected % current_operand == 0 and is_solvable(
        expected // current_operand, operands[0:-1]
    ):
        return True
    if endswith(expected, current_operand) and is_solvable(
        expected // (10 ** digits(current_operand)), operands[0:-1]
    ):
        return True
    else:
        return is_solvable(expected - current_operand, operands[0:-1])


def main():
    # always evaluated left-to-right,
    # so we need to check what was the last operation made
    print(sum([eq[0] for eq in equations if is_solvable(*eq)]))


if __name__ == "__main__":
    main()
