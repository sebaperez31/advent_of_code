import re
from collections import namedtuple
from enum import Enum

class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4
    
class MapInformation:

    def __init__(self):
        self.obstacles_by_row = dict()
        self.obstacles_by_column = dict()
        self.guard_information = None
        self.size = 0
        self.guard_infos = set()
    
    def reset_guard_infos(self):
        self.guard_infos.clear()
        
    def add_obstacle(self, row, column):
        if (row in self.obstacles_by_row):
            self.obstacles_by_row[row].append(column)
        else:
            self.obstacles_by_row[row] = [column]
        
        if (column in self.obstacles_by_column):
            self.obstacles_by_column[column].append(row)
        else:
            self.obstacles_by_column[column] = [row]
    
    def remove_obstacle(self, row, column):
        self.obstacles_by_row[row].remove(column)
        self.obstacles_by_column[column].remove(row)

        
class GuardInformation:
    def __init__(self, row, column, direction):
        self.row = row
        self.column = column
        self.direction = direction

def load_map(filename):
    map_info = MapInformation()
    with open(filename) as map_file:
        for line_number, line_text in enumerate(map_file):
            if line_number == 0:
                map_info.size = len(line_text.rstrip())
            for match in re.finditer("#", line_text):
                row = line_number
                column = match.span()[0]
                map_info.add_obstacle(row, column)
                
            if map_info.guard_information == None:
                for match in re.finditer("\^", line_text):
                    map_info.guard_information = GuardInformation(line_number, match.span()[0], Direction.Up)
    return map_info

def move(map_info : MapInformation):
    guard_info = map_info.guard_information
    initial_position = (guard_info.row, guard_info.column)
    initial_direction = guard_info.direction
    new_guard_infos = []
    match guard_info.direction:
        case Direction.Up:
            if (guard_info.column in map_info.obstacles_by_column):
                rows = list(filter(lambda row : row < guard_info.row, map_info.obstacles_by_column[guard_info.column]))
                if len(rows) > 0:
                    guard_info.row = max(rows) + 1
                    guard_info.direction = Direction.Right
                else:
                    guard_info.row = -1
            else:
                guard_info.row = -1
            new_guard_infos = [GuardInformation(row, guard_info.column, initial_direction) for row in range(initial_position[0], guard_info.row, -1)]
        case Direction.Down:
            if guard_info.column in map_info.obstacles_by_column:
                rows = list(filter(lambda row : row > guard_info.row, map_info.obstacles_by_column[guard_info.column]))
                if len(rows) > 0:
                    guard_info.row = min(rows) - 1
                    guard_info.direction = Direction.Left
                else:
                    guard_info.row = map_info.size
            else:
                guard_info.row = map_info.size
            new_guard_infos = [GuardInformation(row, guard_info.column, initial_direction) for row in range(initial_position[0], guard_info.row, 1)]
        case Direction.Left:
            if guard_info.row in map_info.obstacles_by_row:
                columns = list(filter(lambda col : col < guard_info.column, map_info.obstacles_by_row[guard_info.row]))
                if len(columns) > 0:
                    guard_info.column = max(columns) + 1
                    guard_info.direction = Direction.Up
                else:
                    guard_info.column = -1
            else:
                guard_info.column = -1
            new_guard_infos = [GuardInformation(guard_info.row, column, initial_direction) for column in range(initial_position[1], guard_info.column, -1)]
        case Direction.Right:
            if guard_info.row in map_info.obstacles_by_row:
                columns = list(filter(lambda col : col > guard_info.column, map_info.obstacles_by_row[guard_info.row]))
                if len(columns) > 0:
                    guard_info.column = min(columns) - 1
                    guard_info.direction = Direction.Down
                else:
                    guard_info.column = map_info.size
            else:
                guard_info.column = map_info.size
            new_guard_infos = [GuardInformation(guard_info.row, column, initial_direction) for column in range(initial_position[1], guard_info.column, 1)]

    for new_guard_info in new_guard_infos:
        key = f"{new_guard_info.row}-{new_guard_info.column}-{new_guard_info.direction}"
        if key in map_info.guard_infos:
            # loop detected!
            return None
        else:
            map_info.guard_infos.add(key)

    return new_guard_infos
        

def guard_in_map(map_info):
    return map_info.guard_information.row != -1 and map_info.guard_information.row != map_info.size and map_info.guard_information.column != -1 and map_info.guard_information.column != map_info.size

map_info = load_map("map.txt")
initial_guard_information = GuardInformation(map_info.guard_information.row, map_info.guard_information.column, map_info.guard_information.direction)

positions = set()
while guard_in_map(map_info):
    for guard_info in move(map_info):
        positions.add((guard_info.row, guard_info.column))

print(len(positions))

loop_obstacles = []

positions.remove((initial_guard_information.row,initial_guard_information.column))

for position in positions:

    map_info.guard_information = GuardInformation(initial_guard_information.row, initial_guard_information.column, initial_guard_information.direction)
    map_info.reset_guard_infos()

    map_info.add_obstacle(position[0], position[1])

    while guard_in_map(map_info):
        if move(map_info) == None:
            loop_obstacles.append(position)
            break

    map_info.remove_obstacle(position[0], position[1])

print(len(loop_obstacles))





