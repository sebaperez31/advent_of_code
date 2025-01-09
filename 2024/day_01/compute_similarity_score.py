from collections import Counter

left_list = []
right_list = []
with open('input_lists.txt') as file:
    for line in file:
        ids = [int(id) for id in line.split() if id]
        left_list.append(ids[0])
        right_list.append(ids[1])

score = 0
right_counter = Counter(right_list)
for item in left_list:
    score += item * right_counter[item]

print(score)