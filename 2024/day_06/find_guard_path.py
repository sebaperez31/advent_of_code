import re
from collections import namedtuple
from enum import Enum

class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column
    
    def __hash__(self):
        return hash((self.row, self.column))

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.row == other.row and self.column == other.column
        return False
    
class State:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
    
    def __hash__(self):
        return hash((self.position, int(self.direction)))

    def __eq__(self, other):
        if isinstance(other, State):
            return self.position == other.position and self.direction == other.direction
        return False

class Guard:
    def __init__(self, state):
        self.current_state = state
        self.previous_state = None

    def create_from_file(filename):
        with open(filename) as file:
            for line_number, line_text in enumerate(file):    
                for match in re.finditer("\^", line_text):
                    return Guard(State(Position(line_number, match.span()[0]), Direction.Up))
    
    def move(self, map):
        self.previous_state = State(Position(self.current_state.position.row, self.current_state.position.column), self.current_state.direction)
        match self.current_state.direction:
            case Direction.Up:
                return self.move_up(map)
            case Direction.Down:
                return self.move_down(map)
            case Direction.Left:
                return self.move_left(map)    
            case Direction.Right:
                return self.move_right(map)
            
    def move_up(self, map):
        if (self.current_state.position.column in map.obstacles_by_column):
            rows = list(filter(lambda row : row < self.current_state.position.row, map.obstacles_by_column[self.current_state.position.column]))
            if len(rows) > 0:
                self.current_state.position.row = max(rows) + 1
                self.current_state.direction = Direction.Right
            else:
                self.current_state.position.row = -1
        else:
            self.current_state.position.row = -1
        return [State(Position(row, self.current_state.position.column), self.previous_state.direction) for row in range(self.previous_state.position.row, self.current_state.position.row, -1)]
    
    def move_down(self, map):
        if self.current_state.position.column in map.obstacles_by_column:
            rows = list(filter(lambda row : row > self.current_state.position.row, map.obstacles_by_column[self.current_state.position.column]))
            if len(rows) > 0:
                self.current_state.position.row = min(rows) - 1
                self.current_state.direction = Direction.Left
            else:
                self.current_state.position.row = map.size
        else:
            self.current_state.position.row = map.size
        return [State(Position(row, self.current_state.position.column), self.previous_state.direction) for row in range(self.previous_state.position.row, self.current_state.position.row, 1)]
    
    def move_left(self, map):
        if self.current_state.position.row in map.obstacles_by_row:
            columns = list(filter(lambda col : col < self.current_state.position.column, map.obstacles_by_row[self.current_state.position.row]))
            if len(columns) > 0:
                self.current_state.position.column = max(columns) + 1
                self.current_state.direction = Direction.Up
            else:
                self.current_state.position.column = -1
        else:
            self.current_state.position.column = -1
        return [State(Position(self.current_state.position.row, column), self.previous_state.direction) for column in range(self.previous_state.position.column, self.current_state.position.column, -1)]
    
    def move_right(self, map):
        if self.current_state.position.row in map.obstacles_by_row:
            columns = list(filter(lambda col : col > self.current_state.position.column, map.obstacles_by_row[self.current_state.position.row]))
            if len(columns) > 0:
                self.current_state.position.column = min(columns) - 1
                self.current_state.direction = Direction.Down
            else:
                self.current_state.position.column = map.size
        else:
            self.current_state.position.column = map.size
        return [State(Position(self.current_state.position.row, column), self.previous_state.direction) for column in range(self.previous_state.position.column, self.current_state.position.column, 1)]
    
    def still_in_map(self, map):
        return self.current_state.position.row != -1 and self.current_state.position.row != map.size and self.current_state.position.column != -1 and self.current_state.position.column != map.size
    
class Map:
    def __init__(self):
        self.obstacles_by_row = dict()
        self.obstacles_by_column = dict()
        self.size = 0
        
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

    def create_from_file(filename):
        map = Map()
        with open(filename) as file:
            for line_number, line_text in enumerate(file):
                if line_number == 0:
                    map.size = len(line_text.rstrip())
                for match in re.finditer("#", line_text):
                    row = line_number
                    column = match.span()[0]
                    map.add_obstacle(row, column)
        return map
    

""" def move(map_info):
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

    return new_guard_infos """
        
file = "test_map.txt"
map = Map.create_from_file(file)
guard = Guard.create_from_file(file)
initial_state = State(Position(guard.current_state.position.row, guard.current_state.position.column), guard.current_state.direction)

positions = set()
while guard.still_in_map(map):
    for state in guard.move(map):
        positions.add(state.position)

print(len(positions))


""" loop_obstacles = []

positions.remove((initial_state.position.row,initial_state.position.column))

for position in positions:
    new_guard = Guard(State(Position(initial_state.position.row, initial_state.position.column),initial_state.direction))
    map.add_obstacle(position[0], position[1])

    while new_guard.still_in_map(map):
        for state in guard.move(map):
            # aca hay que hacer algo!!


    map.remove_obstacle(position[0], position[1])

print(len(loop_obstacles)) """