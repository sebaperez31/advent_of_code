import unittest
import re
from enum import Enum

class Operation(Enum) :
    Mul = 1
    Do = 2
    Dont = 3

def get_operation(match):
    if match[2] != '':
        return Operation.Do
    elif match[3] != '':
        return Operation.Dont
    else:
        return Operation.Mul
        
def find_enabled_mul_operations(text):
    result = []
    enabled = True
    for match in re.findall("mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))", text):
        operation = get_operation(match)
        if operation == Operation.Do:
            enabled = True
        elif operation == Operation.Dont:
            enabled = False
        else:
            if enabled:
                result.append((int(match[0]), int(match[1])))
    return result


class FindMulOperationsTests(unittest.TestCase):

    def test_1_by_1(self):
        self.assertEqual(find_enabled_mul_operations("mul(1,1)")[0], (1,1))

    def test_32_by_198(self):
        self.assertEqual(find_enabled_mul_operations("mul(32,198)")[0], (32,198))

    def test_32_by_198_with_noise(self):
        self.assertEqual(find_enabled_mul_operations("mulmulmul(32,198)")[0], (32,198))
    
    def test_32_by_198_and_34_by_12(self):
        result = find_enabled_mul_operations("mulmulmul(32,198)(((mul()mul(34,12))))")
        self.assertEqual(result[0], (32,198))
        self.assertEqual(result[1], (34,12))
    


#if __name__ == '__main__':
#    unittest.main()


sum = 0
with open('memory.txt') as file:
    contenido = file.readlines()
    contenido_sin_saltos = "".join(contenido)
    for mul in find_enabled_mul_operations(contenido_sin_saltos):
        sum += mul[0] * mul[1]

print(sum)

        



    