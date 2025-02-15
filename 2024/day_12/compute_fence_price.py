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

def get_name(map, position):
    return map[position.row, position.column]

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
        self.horizontal_fences_by_row = dict()
        self.vertical_fences_by_column = dict()

    def add_garden(self, garden):
        self.gardens.add(garden)

    def add_gardens(self, new_gardens):
        for new_garden in new_gardens:
            self.add_garden(new_garden)
    
    def compute_price(self):
        return self.get_area() * self.get_number_of_sides()

    def get_area(self):
        return len(self.gardens)

    def get_perimeter(self):
        return len(self.get_fences())

    def get_number_of_horizontal_sides(self, horizontal_fences_in_row_sorted, direction):
        result = 0
        current_column = -2
        for fence_in_row in [f for f in horizontal_fences_in_row_sorted if f.direction == direction]:
            if fence_in_row.position.column - current_column > 1:
                result += 1
            current_column = fence_in_row.position.column
        return result

    def get_number_of_vertical_sides(self, vertical_fences_in_column_sorted, direction):
        result = 0
        current_row = -2
        for fence_in_column in [f for f in vertical_fences_in_column_sorted if f.direction == direction]:
            if fence_in_column.position.row - current_row > 1:
                result += 1
            current_row = fence_in_column.position.row
        return result

    def get_number_of_sides(self):
        self.load_fences_dicts()
        number_of_sides = 0
        
        for horizontal_fences_in_row in self.horizontal_fences_by_row.values():
            horizontal_fences_in_row_sorted = sorted(horizontal_fences_in_row, key = lambda fence : fence.position.column)
            up_sides = self.get_number_of_horizontal_sides(horizontal_fences_in_row_sorted, Direction.Up)
            down_sides = self.get_number_of_horizontal_sides(horizontal_fences_in_row_sorted, Direction.Down)
            number_of_sides += up_sides + down_sides

        for vertical_fences_in_column in self.vertical_fences_by_column.values():
            vertical_fences_in_column_sorted = sorted(vertical_fences_in_column, key = lambda fence : fence.position.row)
            left_sides = self.get_number_of_vertical_sides(vertical_fences_in_column_sorted, Direction.Left)
            right_sides = self.get_number_of_vertical_sides(vertical_fences_in_column_sorted, Direction.Right)
            number_of_sides += left_sides + right_sides
        
        return number_of_sides

    def load_fences_dicts(self):
        for fence in self.get_fences():
            if fence.direction == Direction.Up or fence.direction == Direction.Down:
                # horizontal fence
                self.add_horizontal_fence(fence)    
            else:
                # vertical fence
                self.add_vertical_fence(fence)

    def add_horizontal_fence(self, fence):
        if fence.position.row in self.horizontal_fences_by_row:
            self.horizontal_fences_by_row[fence.position.row].append(fence)
        else:
            self.horizontal_fences_by_row[fence.position.row] = [fence]

    def add_vertical_fence(self, fence):
        if fence.position.column in self.vertical_fences_by_column:
            self.vertical_fences_by_column[fence.position.column].append(fence)
        else:
            self.vertical_fences_by_column[fence.position.column] = [fence]

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
    region_name = get_name(map, position)
    near_garden_position = get_near_garden_position(position, direction)
    near_garden_name = get_name(map, near_garden_position)
    if near_garden_position in processed_positions or near_garden_name != region_name:
        return []

    processed_positions.add(near_garden_position)
    near_garden = Garden(near_garden_name, near_garden_position)
    return [near_garden] + get_near_gardens(near_garden.position, map, map_size, processed_positions)            

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
    
    current_garden = Garden(get_name(map, position), position)
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
    #print(region.name)
    total_price += region.compute_price()

print(total_price)