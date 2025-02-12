import re
from collections import namedtuple
from functools import reduce
import operator
import numpy as np

Robot = namedtuple("Robot", ["px", "py", "vx", "vy"])

def move(robot, times, rows, columns):
    # compute new_px
    new_px = robot.px + (times * robot.vx) % columns
    if new_px < 0:
        new_px += columns
    elif new_px >= columns:
        new_px -= columns

    # compute new_px
    new_py = robot.py + (times * robot.vy) % rows 
    if new_py < 0:
        new_py += rows
    elif new_py >= rows:
        new_py -= rows
    
    return Robot(new_px, new_py, robot.vx, robot.vy)

def get_quadrant(robot, rows, columns):
    x_center = columns // 2
    y_center = rows // 2
    if robot.px < x_center and robot.py < y_center:
        return 0
    elif robot.px > x_center and robot.py < y_center:
        return 1
    elif robot.px < x_center and robot.py > y_center:
        return 2
    elif robot.px > x_center and robot.py > y_center:
        return 3
    else:
        return None

times = 100
rows = 103
columns = 101

robots = []
with open("complete_data.txt") as file:
    for line in file:
        match = re.search(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line)
        px = int(match.group(1))
        py = int(match.group(2))
        vx = int(match.group(3))
        vy = int(match.group(4))
        robots.append(Robot(px, py, vx, vy))

updated_robots = map(lambda robot : move(robot, times, rows, columns), robots)

robots_per_quadrant = {
    0 : 0,
    1 : 0,
    2 : 0,
    3 : 0  
}

for updated_robot in updated_robots:
    quadrant = get_quadrant(updated_robot, rows, columns)
    if quadrant != None:
        robots_per_quadrant[quadrant] = robots_per_quadrant[quadrant] + 1

safety_factor = reduce(operator.mul, robots_per_quadrant.values())
print(safety_factor)

def plot(robots, rows, columns):
    positions = set()
    for robot in robots:
        positions.add((robot.px, robot.py))
    
    plot_robots = False
    # looking for something like:
    # .xxx.
    # .xxx.
    # .xxx.
    for position in positions:
        if  (position[0]-1, position[1])   in positions and  \
            (position[0]+1, position[1])   in positions and \
            (position[0],   position[1]-1) in positions and \
            (position[0],   position[1]+1) in positions and \
            (position[0]-1, position[1]-1) in positions and \
            (position[0]+1, position[1]+1) in positions and \
            (position[0]+1, position[1]-1) in positions and \
            (position[0]-1, position[1]+1) in positions:
            plot_robots = True
            break 
    
    if plot_robots:
        matrix = np.full((rows, columns), ".")
        for robot in robots:
            matrix[robot.py, robot.px] = "x"
        for row in range(rows):
            line = ""
            for column in range(columns):
                line += matrix[row, column]
            print(line)
        input()

times = 1
while True:
    print(f"times = {times}")
    updated_robots = list(map(lambda robot : move(robot, times, rows, columns), robots))
    plot(updated_robots, rows, columns)
    times += 1