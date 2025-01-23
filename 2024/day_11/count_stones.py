#initial_stones = [6563348, 67, 395, 0, 6, 4425, 89567, 739318]
initial_stones = [125, 17]
blinking_times = 25

def transform(stone):
    if stone == 0:
        return [1]
    stone_str = str(stone)
    len_stone_str = len(stone_str) 
    if len_stone_str % 2 == 0:
        return [ int(stone_str[:int(len_stone_str/2)]), int(stone_str[int(len_stone_str/2):]) ]
    return [ stone * 2024 ]

def blink(stone, times):
    if times == 0:
        return 1

    return sum([blink(new_stone, times - 1) for new_stone in transform(stone)])

result = 0
for stone in initial_stones:
    result += blink(stone, blinking_times)

print(result)
