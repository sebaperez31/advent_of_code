from collections import namedtuple
from enum import Enum
import re
from functools import reduce

class InputFileData(Enum):
    ButtonA = 1
    ButtonB = 2
    PricePosition = 3
    NewMachine = 4

Position = namedtuple("Position", ["x", "y"])

Button = namedtuple("Button", ["delta_x", "delta_y"])

ClawMachine = namedtuple("ClawMachine", ["button_a", "button_b", "price_position"])

claw_machines = []
with open("complete_data.txt") as file:
    button_a = None
    button_b = None
    price_position = None
    input_file_data = InputFileData.ButtonA
    for line in file:
        match input_file_data:
            case InputFileData.ButtonA:
                delta_x = int(re.search(r'X\+(\d+)', line).group(1))
                delta_y = int(re.search(r'Y\+(\d+)', line).group(1))
                button_a = Button(delta_x, delta_y)
                input_file_data = InputFileData.ButtonB
            case InputFileData.ButtonB:
                delta_x = int(re.search(r'X\+(\d+)', line).group(1))
                delta_y = int(re.search(r'Y\+(\d+)', line).group(1))
                button_b = Button(delta_x, delta_y)
                input_file_data = InputFileData.PricePosition
            case InputFileData.PricePosition:
                x = int(re.search(r'X=(\d+)', line).group(1)) + 10000000000000
                y = int(re.search(r'Y=(\d+)', line).group(1)) + 10000000000000
                price_position = Position(x, y)
                claw_machines.append(ClawMachine(button_a, button_b, price_position))
                input_file_data = InputFileData.NewMachine
            case InputFileData.NewMachine:
                input_file_data = InputFileData.ButtonA


def get_tokens_for_unique_solution(claw_machine):
    return 1

def get_tokens(claw_machine):
    button_b_denominator = claw_machine.button_a.delta_x * claw_machine.button_b.delta_y - claw_machine.button_a.delta_y * claw_machine.button_b.delta_x 
    if button_b_denominator == 0:
        return 0
    button_b_numerator = claw_machine.button_a.delta_x * claw_machine.price_position.y - claw_machine.button_a.delta_y * claw_machine.price_position.x
    if button_b_numerator % button_b_denominator != 0:
        return 0
    n_button_b = button_b_numerator // button_b_denominator
    button_a_numerator = claw_machine.price_position.x - claw_machine.button_b.delta_x * n_button_b
    if button_a_numerator % claw_machine.button_a.delta_x:
        return 0
    n_button_a = button_a_numerator // claw_machine.button_a.delta_x
    return 3 * n_button_a + 1 * n_button_b

    

tokens = 0
for claw_machine in claw_machines:
    tokens += get_tokens(claw_machine)

print(tokens)
