import numpy as np

def is_safe(report) :
    if (report[0] == report[1]) :
        return False
    ascending = report[0] < report[1]
    for i in range(len(report) - 1) :
        diff = (report[i+1] - report[i]) * (1 if ascending else (-1))
        if (diff < 1 or diff > 3) :
            return False
    return True

safe_reports = 0
with open('reports.txt') as file:
    for line in file:
        report = [int(level) for level in line.split()]
        if is_safe(report) :
            safe_reports += 1
        else :
            for i in range(len(report)) :
                new_report = report.copy()
                new_report.pop(i)
                if is_safe(new_report) :
                    diff = np.array(report[1:]) - np.array(report[:-1])
                    print(f"fixed report {report}, diff {diff}")
                    safe_reports += 1
                    break

print(safe_reports)