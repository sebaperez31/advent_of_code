import re
from itertools import combinations
from collections import namedtuple
import numpy as np

Position = namedtuple("Position", ["row", "column"])

def in_map(position, map_size):
    return position.row >= 0 and position.row < map_size and position.column >= 0 and position.column < map_size

def get_antinodes(antennas, map_size):
    antenna1 = antennas[0]
    antenna2 = antennas[1]
    diff = Position(antenna2.row - antenna1.row, antenna2.column - antenna1.column)
    antinode1 = Position(antenna2.row + diff.row, antenna2.column + diff.column)
    antinode2 = Position(antenna1.row - diff.row, antenna1.column - diff.column)
    antinodes = []
    if in_map(antinode1, map_size):
        antinodes.append(antinode1)
    if in_map(antinode2, map_size):
        antinodes.append(antinode2)
    return antinodes
        
antennas = dict()
map_size = None
with open("complete_map.txt") as file:
    for row, line in enumerate(file):
        if (row == 0):
            map_size = len(line) - 1
        for match in re.finditer("[a-zA-Z0-9]", line):
            column = match.span()[0]
            frequency = match.group()
            if (frequency in antennas):
                antennas[frequency].append(Position(row, column))
            else:
                antennas[frequency] = [Position(row, column)]

antinodes = set()
for frequency, locations in antennas.items():
    for combination in combinations(locations, 2):
        for antinode in get_antinodes(combination, map_size):
            antinodes.add(antinode)

print(len(antinodes))