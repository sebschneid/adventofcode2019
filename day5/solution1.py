import enum
from typing import List, NewType

import numpy as np

# 99: stop
# 1: add from two positions and store in third (next three integers)
# 2: like 1 but multiply
# Next opcode 4 positions later
"""
replace position 1 with the value 12 and replace position 2 with the value 2. What value is left at position 0 after the program halts?
"""

Intcode = NewType("Intcode", List[int])
Opode = NewType("Opcode", int)
DiagnosticCode = NewType("DiagnosticCode", int)


class Mode(enum.Enum):
    POSITION = enum.auto()
    IMMEDIATE = enum.auto()


NUMBER_TO_MODE = {
    0: Mode.POSITION,
    1: Mode.IMMEDIATE,
}


def get_modes(opcode):
    # print(f"Get modes for {opcode}")
    # print("Mode1: ", opcode // 100 % 10)
    first_mode = NUMBER_TO_MODE[opcode // 100 % 10]
    # print("Mode2: ", opcode // 1000 % 10)
    second_mode = NUMBER_TO_MODE[opcode // 1000 % 10]
    # write mode is never IMMEDIATE
    return (first_mode, second_mode, Mode.IMMEDIATE)


def get_values(intcode, position, modes):
    values = [
        intcode[value] if mode == Mode.POSITION else value
        for value, mode in zip(
            [intcode[pos] for pos in range(position + 1, position + 4)], modes
        )
    ]
    return values


def add_next_values(intcode, position, modes):
    first_value, second_value, adress = get_values(intcode, position, modes)
    # print(f"Add {first_value} and {second_value}, store it at position {adress}")
    return (first_value + second_value), adress


def multiply_next_values(intcode, position, modes):
    first_value, second_value, adress = get_values(intcode, position, modes)
    # print(f"Multiply {first_value} and {second_value}, store it at position {adress}")

    return (first_value * second_value), adress


OPCODE_TO_FUNCTION = {
    1: add_next_values,
    2: multiply_next_values,
}


output = []


def evaluate_opcode(opcode, intcode, position):
    # print(f"Evaluate Opcode: {opcode}")
    steps = len(f"{opcode:04d}")
    modes = get_modes(opcode)
    opcode = int(str(opcode)[-2:])
    if opcode in [1, 2]:
        value, adress = OPCODE_TO_FUNCTION[opcode](intcode, position, modes)
        # print(modes)
        return adress, value, steps
    elif opcode in [3, 4]:
        steps = 2
        adress = intcode[position + 1]
        if opcode == 3:
            return adress, USER_INPUT, steps
        else:
            # opcode 4
            output.append(intcode[adress])
            return None, None, steps
    else:
        # print(intcode[position])
        raise ValueError(f"Opcode {opcode} is not in {1, 2, 3, 4}")


# read input intcode
with open("input.txt") as file:
    intcode_start = file.read().rstrip("\n").split(",")
    intcode_start = [int(code) for code in intcode_start]


USER_INPUT = 1


def process_intcode(intcode: Intcode) -> DiagnosticCode:
    # process code
    position = 0
    while position < len(intcode):
        opcode = intcode[position]
        if opcode == 99:
            print(output)
            break
        # print(f"Evaluate: Position={position}, Opcode={opcode}")
        adress, value, steps = evaluate_opcode(opcode, intcode, position)
        # print(f"Result: Adress={adress}, Value={value}, Steps={steps}")
        if adress is not None:
            intcode[adress] = value
        position += steps

    return intcode[0]


print(process_intcode(intcode_start))
