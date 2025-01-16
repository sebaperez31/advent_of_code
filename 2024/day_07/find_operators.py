from itertools import product

def compute(input1, input2, operator):
    match operator:
        case "+":
            return input1 + input2
        case "*":
            return input1 * input2
        case "|":
            return int(str(input1) + str(input2))

operators = ["+", "*", "|"]

final_result = 0
with open("complete_list.txt") as file:
    for line in file:
        items = line.rstrip().split(" ")
        output = int(items[0].replace(":",""))
        input = [int(item) for item in items[1:]]
        operators_options = list(product(operators, repeat=len(input)-1))
        for operators_option in operators_options:
            option_output = input[0]
            for index, operator in enumerate(operators_option):
                option_output = compute(option_output, input[index + 1], operator)
                if (option_output > output):
                    break
            if option_output == output:
                final_result += output
                break
            
print(final_result)



    