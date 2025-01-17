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
        return hash((self.position, self.direction))

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
    
        
file = "map.txt"
map = Map.create_from_file(file)
guard = Guard.create_from_file(file)
initial_position = Position(guard.current_state.position.row, guard.current_state.position.column)

positions = dict()
previous_state = None
while guard.still_in_map(map):
    states = guard.move(map)
    for state in states:
        if (state.position not in positions):
            positions[state.position] = previous_state
        previous_state = state

print(len(positions))

loop_obstacles = []

positions.pop(initial_position)

for obstacle, initial_state in positions.items():
    new_guard = Guard(State(Position(initial_state.position.row, initial_state.position.column), initial_state.direction))
    map.add_obstacle(obstacle.row, obstacle.column)
    states = set()
    while new_guard.still_in_map(map):
        for state in new_guard.move(map):
            if (state in states):
                loop_obstacles.append(obstacle)
                new_guard.current_state.position = Position(-1, -1) # sacamos al guardia del mapa
                break
            else:
                states.add(state)
    map.remove_obstacle(obstacle.row, obstacle.column)

print(len(loop_obstacles))