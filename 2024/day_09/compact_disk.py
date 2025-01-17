from array import array

def disk_to_str(disk):
    result = ""
    for x in disk:
        result += "." if x == -1 else str(x)
    print(result)

disk = []
with open("complete_disk.txt") as file:
    for line in file:
        id = 0
        is_file = True
        for c in line:
            blocks = int(c)
            x = id if is_file else -1
            for i in range(blocks):
                disk.append(x)
            if is_file:
                id += 1
            is_file = not is_file



disk_array = array("i", disk)
i = len(disk_array) - 1
empty_block = 0
while empty_block < i:
    if disk_array[i] == -1:
        i -= 1
    else:
        while disk_array[empty_block] != -1:
            empty_block += 1
            if empty_block == i:
                break

        if empty_block < i:    
            disk_array[empty_block] = disk_array[i]
            disk_array[i] = -1
        else:
            break

result = 0
for index, id in enumerate(disk_array):
    if id != -1:
        result += index * id

print(result)
        

