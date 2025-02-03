from collections import namedtuple
import numpy as np
from enum import Enum

class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

Position = namedtuple("Position", ["row", "column"])

Garden = namedtuple("Garden", ["name", "position"])

Fence = namedtuple("Fence", ["position", "direction"])

def get_near_garden_position(position, direction):
    match direction:
        case Direction.Up:
            return Position(position.row - 1, position.column)
        case Direction.Down:
            return Position(position.row + 1, position.column)
        case Direction.Left:
            return Position(position.row, position.column - 1)
        case Direction.Right:
            return Position(position.row, position.column + 1)

class Region:
    def __init__(self, name):
        self.name = name
        self.gardens = set()

    def add_garden(self, garden):
        self.gardens.add(garden)

    def add_gardens(self, new_gardens):
        for new_garden in new_gardens:
            self.add_garden(new_garden)
    
    def compute_price(self):
        return self.get_area() * self.get_perimeter()

    def get_area(self):
        return len(self.gardens)

    def get_perimeter(self):
        return len(self.get_fences())

    def get_number_of_sides(self):
        return 0

    def get_fences(self):
        fences = []
        for garden in self.gardens:
            if not self.exist_near_garden(garden, Direction.Up):
                fences.append(Fence(garden.position, Direction.Up))
            if not self.exist_near_garden(garden, Direction.Down):
                fences.append(Fence(garden.position, Direction.Down))
            if not self.exist_near_garden(garden, Direction.Left):
                fences.append(Fence(garden.position, Direction.Left))
            if not self.exist_near_garden(garden, Direction.Right):
                fences.append(Fence(garden.position, Direction.Right))
        return fences

    def exist_near_garden(self, current_garden, direction):
        near_garden_position = get_near_garden_position(current_garden.position, direction)
        near_garden = Garden(self.name, near_garden_position)
        return near_garden in self.gardens

def get_near_gardens_from_direction(position, map, map_size, processed_positions, direction):
    region_name = map[position.row, position.column]
    near_garden_position = get_near_garden_position(position, direction)
    near_garden = Garden(map[near_garden_position.row, near_garden_position.column], near_garden_position)
    near_gardens = []
    if near_garden.position not in processed_positions and near_garden.name == region_name:
        processed_positions.add(near_garden.position)
        near_gardens.append(near_garden)
        near_gardens += get_near_gardens(near_garden.position, map, map_size, processed_positions)            
    return near_gardens

def get_near_gardens(position, map, map_size, processed_positions):
    near_gardens = []
    
    if position.row > 0:
        # process up
        near_gardens += get_near_gardens_from_direction(position, map, map_size, processed_positions, Direction.Up)
            
    if position.row < map_size - 1:
        # process down
        near_gardens += get_near_gardens_from_direction(position, map, map_size, processed_positions, Direction.Down)
            
    if position.column > 0:
        # process left
        near_gardens += get_near_gardens_from_direction(position, map, map_size, processed_positions, Direction.Left)

    if position.column < map_size - 1:
        # process right
        near_gardens += get_near_gardens_from_direction(position, map, map_size, processed_positions, Direction.Right)

    return near_gardens 
    
def get_region(position, map, map_size, processed_positions):
    if position in processed_positions:
        return
    
    processed_positions.add(position)
    
    current_garden = Garden(map[position.row, position.column], position)
    region = Region(current_garden.name)
    region.add_garden(current_garden)
    region.add_gardens(get_near_gardens(position, map, map_size, processed_positions))
    return region

map_size = 0
map = None
with open("complete_map.txt") as file:
    row = 0
    for line in file:
        if row == 0:
            map_size = len(line.rstrip())
            map = np.empty((map_size, map_size), dtype="str")

        column = 0
        for c in line.rstrip():
            map[row, column] = c
            column += 1
        
        row += 1

regions = []
processed_positions = set()
for row in range(map_size):
    for column in range(map_size):
        region = get_region(Position(row, column), map, map_size, processed_positions)
        if region != None:
            regions.append(region)

total_price = 0
for region in regions:
    total_price += region.compute_price()

print(total_price)