import math
import re

import numpy as np

file = open("./input.txt", "r")
inputs = file.read().split("\n\n")


class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pressed = None

    def __repr__(self):
        return "{x:%s, y:%s} pushed %s" % (self.x, self.y, self.push)


def round_if_infinite_nines(num):
    if math.isclose(num, round(num), abs_tol=1e-15):
        return round(num)
    return num


def is_whole_number(num):
    return int(num) == num


claw_machines = {}

for input in inputs:
    button_A, button_B, prize = input.split("\n")
    button_pattern = "X((?:\+|-)\d+)|Y((?:\+|-)\d+)"
    buttons = []
    for btn in [button_A, button_B]:
        button_x, button_y = ["".join(x) for x in re.findall(button_pattern, btn)]
        buttons.append(Button(int(button_x), int(button_y)))
    prize_pattern = "X=(\d+)|Y=(\d+)"
    prize_x, prize_y = ["".join(x) for x in re.findall(prize_pattern, prize)]

    claw_machines[(int(prize_x) + 10000000000000, int(prize_y) + 10000000000000)] = (
        buttons
    )

for prize_coord, buttons in claw_machines.items():
    a_button, b_button = buttons
    equation = np.array([[a_button.x, b_button.x], [a_button.y, b_button.y]])
    expected = np.array([prize_coord[0], prize_coord[1]])
    a_pressed, b_pressed = np.linalg.solve(equation, expected)
    a_pressed = round(a_pressed)
    b_pressed = round(b_pressed)
    if (
        a_pressed * a_button.x + b_pressed * b_button.x == prize_coord[0]
        and a_pressed * a_button.y + b_pressed * b_button.y == prize_coord[1]
    ):
        a_button.pressed = a_pressed
        b_button.pressed = b_pressed

spent_tokens = 0
for buttons in claw_machines.values():
    btn_a, btn_b = buttons
    if btn_a.pressed is None:
        continue
    spent_tokens += btn_a.pressed * 3
    spent_tokens += btn_b.pressed * 1

print(spent_tokens)
