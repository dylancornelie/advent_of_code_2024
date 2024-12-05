file = open("./input.txt", "r")
inputs = file.read().split("\n")

splitted_input = [x.split("  ") for x in inputs]
left, right = list(zip(*splitted_input))
sorted_left = [int(x) for x in left]
sorted_right = [int(x) for x in right]

sorted_left.sort()
sorted_right.sort()

result = 0

for (l, r) in zip(sorted_left, sorted_right):
    result += abs(l - r)

print(result)

result = 0
for l in sorted_left:
    occurence = sorted_right.count(l)
    result += occurence * l

print(result)
