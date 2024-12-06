file = open("./input.txt", "r")
inputs = file.read().split("\n")

ordering_rules = []
updates = []

for input in inputs:
    if '|' in input:
        ordering_rules.append(tuple(input.split('|')))
    elif ',' in input:
        updates.append(input.split(','))


def is_update_valid(update):
    rule_index = []
    for (left, right) in ordering_rules:
        try:
            left_index = update.index(left)
            right_index = update.index(right)
            rule_index.append((left_index, right_index))
        except ValueError:
            rule_index.append((None, None))
    rule_index = list(
        filter(lambda r: r[0] is not None and r[1] is not None, rule_index)
    )
    if all(map(lambda r: r[0] < r[1], rule_index)):
        return True, rule_index
    return False, rule_index


total_middle_values = 0
invalid_updates_by_rule_index = {}
for update in updates:
    is_valid, rule_index = is_update_valid(update)
    if is_valid:
        total_middle_values += int(update[len(update) // 2])
    else:
        invalid_updates_by_rule_index[tuple(rule_index)] = update

print(total_middle_values)
corrected_updates = []
for rule_index, update in invalid_updates_by_rule_index.items():
    rule = list(rule_index)
    left_index, right_index = next(filter(lambda r: r[0] > r[1], rule))
    while left_index is not None and right_index is not None:
        try:
            update[left_index], update[right_index] = (
                update[right_index], update[left_index]
            )
            is_valid, rule = is_update_valid(update)
            if is_valid:
                break
            left_index, right_index = next(filter(lambda r: r[0] > r[1], rule))
        except StopIteration:
            left_index, right_index = None, None
    corrected_updates.append(update)
total_middle_values = 0

for update in corrected_updates:
    total_middle_values += int(update[(len(update) // 2)])

print(total_middle_values)
