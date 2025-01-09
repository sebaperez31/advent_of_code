import re

def init_line(size):  
    return "." * size

puzzle = []
with open("puzzle.txt") as puzzle_file:
    for line in puzzle_file:
        puzzle.append(line.rstrip())

#puzzle = ["1234",
#          "5678",
#          "90AB",
#          "CDEF"]

size = len(puzzle[0])

xmas_count = 0
for i in range(size):
    horizontal = puzzle[i]
    vertical = ""
    angle_45_sup = ""
    angle_45_inf = ""
    angle_minus_45_sup = ""
    angle_minus_45_inf = ""

    if (i == 0):
        for j in range(size) :
            vertical += puzzle[j][0]
            angle_45_sup += puzzle[size - j - 1][j]
            angle_minus_45_sup += puzzle[j][j]
    else:
        for j in range(size) :
            vertical += puzzle[j][i]
            if (size - j - 1 - i) >= 0:
                angle_45_sup += puzzle[size - j - 1 - i][j]
            if (j + i) < size:
                angle_45_inf += puzzle[size - j - 1][j + i]
                angle_minus_45_sup += puzzle[j][i + j]   
                angle_minus_45_inf += puzzle[i + j][j]

    xmas_horizontal = len(re.findall("XMAS", horizontal)) + len(re.findall("SAMX", horizontal))
    xmas_vertical = len(re.findall("XMAS", vertical)) + len(re.findall("SAMX", vertical))
    xmas_angle_45_sup = len(re.findall("XMAS", angle_45_sup)) + len(re.findall("SAMX", angle_45_sup))
    xmas_angle_45_inf = len(re.findall("XMAS", angle_45_inf)) + len(re.findall("SAMX", angle_45_inf))
    xmas_angle_minus_45_sup = len(re.findall("XMAS", angle_minus_45_sup)) + len(re.findall("SAMX", angle_minus_45_sup))
    xmas_angle_minus_45_inf = len(re.findall("XMAS", angle_minus_45_inf)) + len(re.findall("SAMX", angle_minus_45_inf))

    print(f"iteration {i}")
    print(f"horizontal {horizontal} -> count {xmas_horizontal}")
    print(f"vertical {vertical} -> count {xmas_vertical}")
    print(f"angle_45_sup {angle_45_sup} -> count {xmas_angle_45_sup}")
    print(f"angle_45_inf {angle_45_inf} -> count {xmas_angle_45_inf}")
    print(f"angle_minus_45_sup {angle_minus_45_sup} -> count {xmas_angle_minus_45_sup}")
    print(f"angle_minus_45_inf {angle_minus_45_inf} -> count {xmas_angle_minus_45_inf}")
    print("")

    xmas_count += xmas_horizontal
    xmas_count += xmas_vertical
    xmas_count += xmas_angle_45_sup
    xmas_count += xmas_angle_45_inf
    xmas_count += xmas_angle_minus_45_sup
    xmas_count += xmas_angle_minus_45_inf

print(xmas_count)