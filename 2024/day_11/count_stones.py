initial_stones = [6563348, 67, 395, 0, 6, 4425, 89567, 739318]
blinking_times = 75

def transform(stone):
    if stone == 0:
        return [1]
    stone_str = str(stone)
    len_stone_str = len(stone_str) 
    if len_stone_str % 2 == 0:
        return [ int(stone_str[:int(len_stone_str/2)]), int(stone_str[int(len_stone_str/2):]) ]
    return [ stone * 2024 ]

def blink(stone, times, results_dict):
    if times == 0:
        return 1

    if (stone, times) in results_dict:
        return results_dict[(stone, times)]

    result = sum([blink(new_stone, times - 1, results_dict) for new_stone in transform(stone)])
    results_dict[(stone, times)] = result
    return result

result = 0
results_dict = dict()
for stone in initial_stones:
    result += blink(stone, blinking_times, results_dict)

print(len(results_dict))
print(result)
