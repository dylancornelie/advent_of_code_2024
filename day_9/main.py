file = open("./input.txt", "r")
disk_map = list(file.read())

hard_drive_representation = []
file_id = 0

for index, digit in enumerate(disk_map):
    if index % 2 == 0:
        # It's a file
        hard_drive_representation.extend([file_id for _ in range(int(digit))])
        file_id += 1
    else:
        # It's free space
        hard_drive_representation.extend(["." for _ in range(int(digit))])

contiguous_hard_drive = hard_drive_representation[:]
current_index = 0
reversed_index = -1
while current_index < len(contiguous_hard_drive):
    current_element = contiguous_hard_drive[current_index]
    if current_element == ".":
        # Retrieve the last file ID from the end
        element_from_back = None
        while (
            abs(reversed_index) < len(contiguous_hard_drive)
            and len(contiguous_hard_drive) + reversed_index > current_index
        ):
            element_from_back = contiguous_hard_drive[reversed_index]
            reversed_index -= 1
            if element_from_back != ".":
                break
        # Swape element
        if element_from_back is not None:
            (
                contiguous_hard_drive[current_index],
                contiguous_hard_drive[reversed_index + 1],
            ) = (
                contiguous_hard_drive[reversed_index + 1],
                contiguous_hard_drive[current_index],
            )
    current_index += 1

checksum = sum(
    [
        index * int(data)
        for (index, data) in enumerate(
            filter(lambda x: x != ".", contiguous_hard_drive)
        )
    ]
)
print("Part 1 result := %s" % checksum)


class File:
    has_been_sorted = False

    def __init__(
        self,
        file_id,
        file_size,
        file_pos,
    ):
        self.file_id = file_id
        self.file_size = file_size
        self.file_pos = file_pos

    def __str__(self):
        return "(file_id:%s, file_size:%s, file_pos:%s, sorted:%s)" % (
            self.file_id,
            self.file_size,
            self.file_pos,
            self.has_been_sorted,
        )

    def __repr__(self):
        return self.__str__()


def get_file_size(starting_position, file_id):
    file_size = 0
    current_file = file_id
    current_position = starting_position
    while current_file == file_id and current_position < len(hard_drive_representation):
        file_size += 1
        current_position += 1
        if current_position < len(hard_drive_representation):
            current_file = hard_drive_representation[current_position]
    return file_size


seen_file_id = set()
parsed_hard_drive = []
for pos, file in enumerate(hard_drive_representation):
    if file != "." and file not in seen_file_id:
        parsed_hard_drive.append(
            File(
                file_id=file,
                file_size=get_file_size(pos, file),
                file_pos=pos,
            )
        )
        seen_file_id.add(file)

defragmented_hard_drive = hard_drive_representation[:]
current_index = 0
while current_index < len(defragmented_hard_drive):
    current_element = defragmented_hard_drive[current_index]
    if current_element != "." and current_element != "|":
        matching_file_repr = next(
            iter(
                filter(
                    lambda x: x.file_id == current_element,
                    parsed_hard_drive,
                )
            )
        )
        matching_file_repr.has_been_sorted = True
    if current_element == ".":
        # Count the number of consecutive dot
        dot_size = get_file_size(current_index, ".")
        # Filter the page left to sort and with a matching size
        file_result = None
        try:
            file_result = max(
                filter(
                    lambda x: not x.has_been_sorted and x.file_size <= dot_size,
                    parsed_hard_drive,
                ),
                key=lambda x: x.file_id,
            )
            file_result.has_been_sorted = True
        except ValueError:
            pass
        # Switch dot to file id
        if file_result is not None:
            for x in range(file_result.file_size):
                defragmented_hard_drive[current_index + x] = file_result.file_id
                defragmented_hard_drive[file_result.file_pos + x] = "|"
    current_index += 1

# print("".join(map(lambda x: str(x), defragmented_hard_drive)))

checksum = sum(
    [
        index * int(data)
        for (index, data) in enumerate(defragmented_hard_drive)
        if data not in [".", "|"]
    ]
)
print("Part 2 result := %s" % checksum)
