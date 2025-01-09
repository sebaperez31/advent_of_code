import numpy as np
import unittest
from enum import Enum
from collections import Counter
import datetime

class Slope(Enum) :
    Positive = 1
    Constant = 2
    Negative = 3

def get_slope(diff):
    if (diff > 0) :
        return Slope.Positive
    elif (diff == 0) :
        return Slope.Constant
    else :
        return Slope.Negative

def is_slope_fixeable(report):
    diffs = np.array(report[1:]) - np.array(report[:-1])
    slopes = [get_slope(diff) for diff in diffs]
    slopes_counter = Counter(slopes)
    constants = slopes_counter.get(Slope.Constant) if slopes_counter.get(Slope.Constant) != None else 0
    positives = slopes_counter.get(Slope.Positive) if slopes_counter.get(Slope.Positive) != None else 0
    negatives = slopes_counter.get(Slope.Negative) if slopes_counter.get(Slope.Negative) != None else 0

    most_common_slope = slopes_counter.most_common(1)[0][0]
    if most_common_slope == Slope.Constant :
        return False
    elif most_common_slope == Slope.Positive :
        return constants + negatives <= 1
    else:
        return constants + positives <= 1


def is_diff_abs_fixeable(report):
    diffs = np.array(report[1:]) - np.array(report[:-1])
    index_errors = [index for index, diff in enumerate(diffs) if abs(diff) > 3]
    if len(index_errors) > 2 :
        # solo es posible fixear dos errores
        return False
    elif len(index_errors) == 2:
        # solo puedo fixear 2 si son consecutivos
        return abs(index_errors[0] - index_errors[1]) == 1
    else:
        # un error podria ser arreglado
        return True


def is_safe(report, allow_fix):
    diffs = np.array(report[1:]) - np.array(report[:-1])
    slopes = [get_slope(diff) for diff in diffs]
    slopes_counter = Counter(slopes)
    slope_safe = True
    if slopes_counter.get(Slope.Constant) != None:
        slope_safe = False
    if len(slopes_counter.keys()) > 1 :
        slope_safe = False
    
    diff_abs_safe = len([diff for diff in diffs if abs(diff) > 3]) == 0

    if slope_safe and diff_abs_safe:
        return True
    elif not allow_fix:
        return False
    else:
        if not is_slope_fixeable(report) or not is_diff_abs_fixeable(report):
            return False

        if slope_safe:
            # el error que puedo arreglar es un salto grande al principio o al final, ni en el medio ni en las dos puntas al mismo tiempo
            left_error = abs(diffs[0]) > 3
            right_error = abs(diffs[-1]) > 3
            middle_error = len([diff for diff in diffs[1:-1] if abs(diff) > 3]) > 0
            if middle_error or (left_error and right_error):
                return False
            else:
                return True
        else:
            # buscamos el error de pendiente
            most_common_slope = slopes_counter.most_common(1)[0][0]
            slope_error_index = [index for index, slope in enumerate(slopes) if slope != most_common_slope][0]
            left_error_index = slope_error_index
            right_error_index = slope_error_index + 1

            if diff_abs_safe:
                if left_error_index == 0:
                    return True
                elif right_error_index == (len(report) - 1) :
                    return True
                else:
                    left_fix_diff = report[left_error_index + 1] - report[left_error_index - 1]
                    right_fix_diff = report[right_error_index + 1] - report[right_error_index - 1]
                    return (get_slope(left_fix_diff) == most_common_slope and abs(left_fix_diff) <=3) or (get_slope(right_fix_diff) == most_common_slope and abs(right_fix_diff) <=3)

            else:
                left_fixed_report = report.copy()
                left_fixed_report.pop(left_error_index)

                right_fixed_report = report.copy()
                right_fixed_report.pop(right_error_index)

                return is_safe(left_fixed_report, False) or is_safe(right_fixed_report, False)


class TestReportSafety(unittest.TestCase):
    def test_safe_ascending(self):
        self.assertEqual(is_safe([1,2,3,4,5], False), True)

    def test_safe_descending(self):
        self.assertEqual(is_safe([5,4,3,2,1], False), True)

    def test_unsafe_one_constant(self):
        self.assertEqual(is_safe([1,1,3,4,5], False), False)

    def test_unsafe_ascending_but_descending_at_the_end(self):
        self.assertEqual(is_safe([1,2,3,4,3], False), False)
    
    def test_unsafe_ascending_but_descending_at_the_begining(self):
        self.assertEqual(is_safe([3,2,3,4,3], False), False)

    def test_safe_with_fix_correct_positive_slope_big_diff_at_the_begining(self):
        self.assertEqual(is_safe([1,5,6,7,8], True), True)
    
    def test_safe_with_fix_correct_positive_slope_big_diff_at_the_end(self):
        self.assertEqual(is_safe([4,5,6,7,11], True), True)

    def test_unsafe_with_fix_correct_positive_slope_big_diff_at_the_end_and_at_the_begining(self):
        self.assertEqual(is_safe([1,5,6,7,11], True), False)

    def test_unsafe_with_fix_correct_positive_slope_big_diff_in_middle(self):
        self.assertEqual(is_safe([4,5,10,11,12], True), False)

    def test_safe_with_fix_correct_positive_slope_big_diff_at_the_end(self):
        self.assertEqual(is_safe([4,5,6,7,11], True), True)

    def test_file_no_allow_fixing(self):
        safe_reports = 0
        with open('reports.txt') as file:
            for line in file:
                report = [int(level) for level in line.split()]
                if is_safe(report, False) :
                    safe_reports += 1
        self.assertEqual(safe_reports, 483)

    def test_file_allow_fixing(self):
        safe_reports = 0
        with open('reports.txt') as file:
            for line in file:
                report = [int(level) for level in line.split()]
                if is_safe(report, True) :
                    safe_reports += 1
        self.assertEqual(safe_reports, 528)

class TestFixeableDiffEvaluation(unittest.TestCase):
    def test_fixeable_diff_at_the_begining(self):
        self.assertEqual(is_diff_abs_fixeable([1,8,9,10,11]), True)

    def test_fixeable_diff_at_the_end(self):
        self.assertEqual(is_diff_abs_fixeable([7,8,9,10,14]), True)

    def test_fixeable_diff_at_the_middle(self):
        self.assertEqual(is_diff_abs_fixeable([7,8,9,13,14]), True)

    def test_fixeable_diff_two_consecutive_errors(self):
        self.assertEqual(is_diff_abs_fixeable([7,8,15,9,10]), True)

    def test_not_fixeable_diff_two_non_consecutive_errors(self):
        self.assertEqual(is_diff_abs_fixeable([7,8,15,16,20]), False)

    def test_not_fixeable_diff_three_errors(self):
        self.assertEqual(is_diff_abs_fixeable([7,8,15,16,20,21,27]), False)

class TestFixeableSlopeEvaluation(unittest.TestCase):
    def test_fixeable_slope_one_error(self):
        self.assertEqual(is_slope_fixeable([1,4,5,4,6]), True)

    def test_non_fixeable_slope_two_errors(self):
        self.assertEqual(is_slope_fixeable([1,4,5,4,6,2]), False)

#if __name__ == '__main__':
#    unittest.main()

start = datetime.datetime.now()
safe_reports = 0
with open('reports.txt') as file:
    for line in file:
        report = [int(level) for level in line.split()]
        if is_safe(report, True) :
            safe_reports += 1
end = datetime.datetime.now()
print(end - start)