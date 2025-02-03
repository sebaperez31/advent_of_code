from collections import namedtuple
import numpy as np
from enum import Enum

class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4

Position = namedtuple("Position", ["row", "column"])

GardenPlot = namedtuple("GardenPlot", ["name", "row", "column"])

Fence = namedtuple("Fence", ["row", "column", "direction"])

def get_near_garden_plot_position(row, column, direction):
    match direction:
        case Direction.Up:
            return Position(row - 1, column)
        case Direction.Down:
            return Position(row + 1, column)
        case Direction.Left:
            return Position(row, column - 1)
        case Direction.Right:
            return Position(row, column + 1)

class Region:
    def __init__(self, name):
        self.name = name
        self.garden_plots = set()

    def add_garden_plot(self, garden_plot):
        self.garden_plots.add(garden_plot)

    def add_garden_plots(self, new_garden_plots):
        for new_garden_plot in new_garden_plots:
            self.add_garden_plot(new_garden_plot)
    
    def compute_price(self):
        return self.get_area() * self.get_perimeter()

    def get_area(self):
        return len(self.garden_plots)

    def get_perimeter(self):
        return len(self.get_fences())

    def get_number_of_sides(self):
        return 0

    def get_fences(self):
        fences = []
        for garden_plot in self.garden_plots:
            if not self.exist_near_garden_plot(garden_plot, Direction.Up):
                fences.append(Fence(garden_plot.row, garden_plot.column, Direction.Up))
            if not self.exist_near_garden_plot(garden_plot, Direction.Down):
                fences.append(Fence(garden_plot.row, garden_plot.column, Direction.Down))
            if not self.exist_near_garden_plot(garden_plot, Direction.Left):
                fences.append(Fence(garden_plot.row, garden_plot.column, Direction.Left))
            if not self.exist_near_garden_plot(garden_plot, Direction.Right):
                fences.append(Fence(garden_plot.row, garden_plot.column, Direction.Right))
        return fences

    def exist_near_garden_plot(self, garden_plot, direction):
        near_garden_plot_position = get_near_garden_plot_position(garden_plot.row, garden_plot.column, direction)
        near_garden_plot = GardenPlot(self.name, near_garden_plot_position.row, near_garden_plot_position.column)
        return near_garden_plot in self.garden_plots

def get_near_garden_plots_from_direction(row, column, map, map_size, processed_garden_plots, direction):
    region_name = map[row, column]
    near_garden_plot_position = get_near_garden_plot_position(row, column, direction)
    near_garden_plot = GardenPlot(map[near_garden_plot_position.row, near_garden_plot_position.column], near_garden_plot_position.row, near_garden_plot_position.column)
    near_garden_plots = []
    if near_garden_plot not in processed_garden_plots and near_garden_plot.name == region_name:
        processed_garden_plots.add(near_garden_plot)
        near_garden_plots.append(near_garden_plot)
        near_garden_plots += get_near_garden_plots(near_garden_plot.row, near_garden_plot.column, map, map_size, processed_garden_plots)            
    return near_garden_plots

def get_near_garden_plots(row, column, map, map_size, processed_garden_plots):
    near_garden_plots = []
    
    if row > 0:
        # process up
        near_garden_plots += get_near_garden_plots_from_direction(row, column, map, map_size, processed_garden_plots, Direction.Up)
            
    if row < map_size - 1:
        # process down
        near_garden_plots += get_near_garden_plots_from_direction(row, column, map, map_size, processed_garden_plots, Direction.Down)
            
    if column > 0:
        # process left
        near_garden_plots += get_near_garden_plots_from_direction(row, column, map, map_size, processed_garden_plots, Direction.Left)

    if column < map_size - 1:
        # process right
        near_garden_plots += get_near_garden_plots_from_direction(row, column, map, map_size, processed_garden_plots, Direction.Right)

    return near_garden_plots 
    
def get_region(row, column, map, map_size, processed_garden_plots):
    current_garden_plot = GardenPlot(map[row, column], row, column)
    if current_garden_plot in processed_garden_plots:
        return
    processed_garden_plots.add(current_garden_plot)
    region = Region(map[row, column])
    region.add_garden_plot(current_garden_plot)
    region.add_garden_plots(get_near_garden_plots(row, column, map, map_size, processed_garden_plots))
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
processed_garden_plots = set()
for row in range(map_size):
    for column in range(map_size):
        region = get_region(row, column, map, map_size, processed_garden_plots)
        if region != None:
            regions.append(region)

total_price = 0
for region in regions:
    total_price += region.compute_price()

print(total_price)