
def is_xmas(puzzle, i, j):
    if puzzle[i][j] != 'A':
        return False
    
    # validate 45 degrees
    if (puzzle[i+1][j-1] == "M" and puzzle[i-1][j+1] == "S") or (puzzle[i+1][j-1] == "S" and puzzle[i-1][j+1] == "M"):
        # validate -45 degress
        if (puzzle[i-1][j-1] == "M" and puzzle[i+1][j+1] == "S") or (puzzle[i-1][j-1] == "S" and puzzle[i+1][j+1] == "M"):
            return True
        else:
            return False
    else:
        return False

    
puzzle = []
with open("puzzle.txt") as puzzle_file:
    for line in puzzle_file:
        puzzle.append(line.rstrip())

size = len(puzzle[0])

xmas_count = 0
for i in range(1, size - 1):
    for j in range(1, size - 1):
        if is_xmas(puzzle, i, j):
            xmas_count += 1


print(xmas_count)