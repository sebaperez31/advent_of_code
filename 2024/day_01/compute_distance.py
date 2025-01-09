import bisect

left_list = []
right_list = []
with open('input_lists.txt') as file:
    for line in file:
        ids = [int(id) for id in line.split() if id]
        bisect.insort(left_list, ids[0])
        bisect.insort(right_list, ids[1])

distance = 0
for i in range(len(left_list)):
    distance += abs(left_list[i] - right_list[i])

print(distance)