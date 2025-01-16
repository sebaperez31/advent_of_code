from itertools import product

operators = ["+", "*", "|"]

calibration = 0
with open("complete_list.txt") as file:
    for line in file:
        items = line.rstrip().split(" ")
        result = int(items[0].replace(":",""))
        values = [int(item) for item in items[1:]]
        options = list(product(operators, repeat=len(values)-1))
        for option in options:
            option_result = values[0]
            for index, operator in enumerate(option):
                match operator:
                    case "+":
                        option_result = option_result + values[index + 1]
                    case "*":
                        option_result = option_result * values[index + 1]
                    case "|":
                        option_result = int(str(option_result) + str(values[index + 1]))
                if (option_result > result):
                    break
            if option_result == result:
                calibration += result
                break
            

print(calibration)



    