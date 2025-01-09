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


class TestPrinting(unittest.TestCase):

    def setUp(self):
        self.rules = []
        with open("test_rules.txt") as rules_file:
            for line in rules_file:
                splited_line = line.split("|")
                self.rules.append((int(splited_line[0]), int(splited_line[1])))

    def test_basic_one_page_result_true(self):
        self.assertEqual(check_printing([(1,2)], [1]), True)

    def test_basic_two_pages_result_true(self):
        self.assertEqual(check_printing([(1,2)], [1,2]), True)

    def test_basic_two_pages_result_false(self):
        self.assertEqual(check_printing([(1,2)], [2,1]), False)
        
    def test1(self):
        self.assertEqual(check_printing(self.rules, [75,47,61,53,29]), True)

    def test2(self):
        self.assertEqual(check_printing(self.rules, [97,61,53,29,13]), True)

    def test3(self):
        self.assertEqual(check_printing(self.rules, [75,29,13]), True)

    def test4(self):
        self.assertEqual(check_printing(self.rules, [75,97,47,61,53]), False)

    def test5(self):
        self.assertEqual(check_printing(self.rules, [61,13,29]), False)
    
    def test6(self):
        self.assertEqual(check_printing(self.rules, [97,13,75,29,47]), False)


#if __name__ == '__main__':
#    unittest.main()

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
    if check_printing(rules, printing):
        result += printing[int((len(printing) - 1) / 2)]

print(result)