import re
from itertools import combinations
from collections import namedtuple
import numpy as np

Position = namedtuple("Position", ["row", "column"])

def in_map(position, map_size):
    return position[0] >= 0 and position[0] < map_size and position[1] >= 0 and position[1] < map_size

def compute_antinodes(antenna, diff, map_size):
    antinodes = []
    i = 0
    while True:
        antinode = antenna + i * diff
        if in_map(antinode, map_size):
            antinodes.append(Position(antinode[0], antinode[1]))
            i += 1
        else:
            break
    return antinodes

def get_antinodes(antennas, map_size):
    antenna1 = np.array(antennas[0])
    antenna2 = np.array(antennas[1])
    diff = antenna2 - antenna1
    antinodes = []
    antinodes.extend(compute_antinodes(antenna1, -diff, map_size))
    antinodes.extend(compute_antinodes(antenna2,  diff, map_size))
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