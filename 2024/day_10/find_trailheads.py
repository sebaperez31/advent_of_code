import numpy as np
from collections import namedtuple

Position = namedtuple("Position", ["row", "column"])

def get_next_positions(current_position, map, map_size):
    next_positions = []
    if current_position.row > 0:
        up = Position(current_position.row - 1, current_position.column)
        if map[up.row, up.column] - map[current_position.row, current_position.column] == 1:
            next_positions.append(up)
    
    if current_position.row < map_size - 1:
        down = Position(current_position.row + 1, current_position.column)
        if map[down.row, down.column] - map[current_position.row, current_position.column] == 1:
            next_positions.append(down)

    if current_position.column > 0:
        right = Position(current_position.row, current_position.column - 1)
        if map[right.row, right.column] - map[current_position.row, current_position.column] == 1:
            next_positions.append(right)

    if current_position.column < map_size - 1:
        left = Position(current_position.row, current_position.column + 1)
        if map[left.row, left.column] - map[current_position.row, current_position.column] == 1:
            next_positions.append(left)
    
    return next_positions

def move_up(current_position, map, map_size):
    if map[current_position.row, current_position.column] == 9:
        return [current_position]
    else:
        result = []
        for next_position in get_next_positions(current_position, map, map_size):
            result += move_up(next_position, map, map_size)
        return result
    
map = None
row = 0
size = 0
with open("complete_map.txt") as file:
    for line in file:
        if row == 0:
            size = len(line.rstrip())
            map = np.zeros((size, size), dtype=int)

        for column, c in enumerate(line.rstrip()):
            map[row, column] = int(c)
        
        row += 1

score = 0
for i in range(size):
    for j in range(size):
        if map[i,j] == 0:
            score += len(move_up(Position(i,j), map, size))

print(score)