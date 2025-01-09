import unittest

def check_printing(rules, pages):
    rules_dict = dict()
    for rule in rules:
        first_page = rule[0]
        second_page = rule[1]
        if (second_page in rules_dict):
            rules_dict[second_page].append(first_page)
        else:
            rules_dict[second_page] = [first_page]

    for index in range(len(pages) - 1):
        current_page = pages[index]
        if (current_page in rules_dict):
            prev_pages_rules = rules_dict[current_page]
            next_pages = pages[(index+1):]
            for prev_page_rule in prev_pages_rules:
                if (prev_page_rule in next_pages):
                    return False

    return True

def find_correct_position(rules_dict, pages, index):
    if (pages[index] not in rules_dict):
        return index
    
    prev_pages_rules = rules_dict[pages[index]]
    for j in range(len(pages) - 1, index, -1):
        if (pages[j] in prev_pages_rules):
            return j
    
    return index
        
def fix_printing(rules, pages):
    rules_dict = dict()
    for rule in rules:
        first_page = rule[0]
        second_page = rule[1]
        if (second_page in rules_dict):
            rules_dict[second_page].append(first_page)
        else:
            rules_dict[second_page] = [first_page]

    result = pages.copy()
    if len(pages) == 1:
        return result
    
    start = len(result) - 2
    while start >= 0:
        for index in range(start, -1, -1):
            correct_position = find_correct_position(rules_dict, result, index)
            start = correct_position - 1
            if correct_position != index:
                page = result[index]
                result.pop(index)
                result.insert(correct_position, page)
                break

    return result


class TestPrinting(unittest.TestCase):

    def setUp(self):
        self.rules = []
        with open("test_rules.txt") as rules_file:
            for line in rules_file:
                splited_line = line.split("|")
                self.rules.append((int(splited_line[0]), int(splited_line[1])))

    def test_basic_one_page_correct(self):
        self.assertEqual(fix_printing([(1,2)], [1]), [1])

    def test_basic_two_pages_correct(self):
        self.assertEqual(fix_printing([(1,2)], [1,2]), [1,2])

    def test_basic_two_pages_incorrect(self):
        self.assertEqual(fix_printing([(1,2)], [2,1]), [1,2])
        
    def test1(self):
        self.assertEqual(fix_printing(self.rules, [75,47,61,53,29]), [75,47,61,53,29])

    def test2(self):
        self.assertEqual(fix_printing(self.rules, [97,61,53,29,13]), [97,61,53,29,13])

    def test3(self):
        self.assertEqual(fix_printing(self.rules, [75,29,13]), [75,29,13])

    def test4(self):
        self.assertEqual(fix_printing(self.rules, [75,97,47,61,53]), [97,75,47,61,53])

    def test5(self):
        self.assertEqual(fix_printing(self.rules, [61,13,29]), [61,29,13])

    def test6(self):
        self.assertEqual(fix_printing(self.rules, [97,13,75,29,47]), [97,75,47,29,13])
    
    

""" 
if __name__ == '__main__':
    unittest.main() """

rules = []
with open("rules.txt") as rules_file:
    for line in rules_file:
        splited_line = line.split("|")
        rules.append((int(splited_line[0]), int(splited_line[1])))

printings = []
with open("printings.txt") as printings_file:
    for line in printings_file:
        splited_line = line.rstrip().split(",")
        printings.append([int(page) for page in splited_line])

result = 0
for printing in printings:
    if not check_printing(rules, printing):
        fixed_printing = fix_printing(rules, printing)
        result += fixed_printing[int((len(fixed_printing) - 1) / 2)]

print(result)