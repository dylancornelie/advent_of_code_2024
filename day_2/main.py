file = open("./input.txt", "r")
inputs = file.read().split("\n")

safe_reports_count = 0


def is_report_safe(levels):
    is_decreasing = None
    safe = True
    for (l0, l1) in zip(levels, levels[1:]):
        if abs(l0 - l1) not in set([1, 2, 3]):
            safe = False
            break
        if is_decreasing is None:
            is_decreasing = l0 > l1
        elif is_decreasing and l0 < l1:
            safe = False
            break
        elif not is_decreasing and l0 > l1:
            safe = False
            break
    return safe


for report in inputs:
    levels = [int(x) for x in report.split(" ")]
    if is_report_safe(levels):
        safe_reports_count += 1

print(safe_reports_count)
safe_reports_count = 0

for report in inputs:
    levels = [int(x) for x in report.split(" ")]
    index_to_remove = 0
    is_safe = is_report_safe(levels)
    while not is_safe and index_to_remove != len(levels):
        copy_level = levels.copy()
        del copy_level[index_to_remove]
        is_safe = is_report_safe(copy_level)
        index_to_remove += 1
    if is_safe:
        safe_reports_count += 1

print(safe_reports_count)
