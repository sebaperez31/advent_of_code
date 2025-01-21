from array import array
from collections import namedtuple

def find_empty_space(disk_array, blocks_needed):
    i = 0
    blocks = 0
    while i < len(disk_array):
        if disk_array[i] == -1:
            blocks += 1
            if blocks == blocks_needed:
                return i - blocks + 1
        else:
            blocks = 0
        i += 1

    return -1

def disk_to_str(disk):
    result = ""
    for x in disk:
        result += "." if x == -1 else str(x)
    print(result)

class File:
    def __init__(self, file_id, blocks, start_index):
        self.file_id = file_id
        self.blocks = blocks
        self.start_index = start_index

    def __str__(self):
        return f"file_id={self.file_id}, blocks={self.blocks}, start_index={self.start_index}"

        
disk = []
files = []

with open("complete_disk.txt") as file:
    for line in file:
        id = 0
        is_file = True
        start_index = 0
        for c in line:
            blocks = int(c)
            x = id if is_file else -1
            for i in range(blocks):
                disk.append(x)
            if is_file:
                files.append(File(x, blocks, start_index))
                id += 1
            is_file = not is_file
            start_index += blocks


disk_array = array("i", disk)

for file in reversed(files):
    empty_space_start_index = find_empty_space(disk_array, file.blocks)
    if empty_space_start_index != -1 and empty_space_start_index < file.start_index:    
        for i in range(file.blocks):
            disk_array[empty_space_start_index + i] = file.file_id
            disk_array[file.start_index + i] = -1


result = 0
for index, id in enumerate(disk_array):
    if id != -1:
        result += index * id


print(result)
