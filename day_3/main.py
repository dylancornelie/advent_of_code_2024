import re

file = open("./input.txt", "r")
inputs = file.read().split("\n")

result = 0
for input in inputs:
    matches = re.findall(
        'mul\((\d{1,3}),(\d{1,3})\)',
        input
    )
    for (left, right) in matches:
        result += int(left) * int(right)

print(result)

result = 0
do_multiply = True
for input in inputs:
    matches = re.findall(
        'mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don\'t\(\))',
        input
    )
    for match in matches:
        left, right, do, dont = match
        if do_multiply and left and right:
            result += int(left) * int(right)
        if do:
            do_multiply = True
        if dont:
            do_multiply = False

print(result)
