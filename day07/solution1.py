# five Ampliiers connected in Series
# receive Input, produce output signal
# 1 -> 2 -> 3 -> 4 -> 5

import enum
import itertools
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


def add_next_values(first, second, third):
    return (first + second), third


def multiply_next_values(first, second, third):
    return (first * second), third


def less_than(first, second, third):
    if first < second:
        return 1, third
    return 0, third


def equals(first, second, third):
    if first == second:
        return 1, third
    return 0, third


def evaluate_opcode(opcode, intcode, position, inputs):
    # print(f"Evaluate Opcode: {opcode}")
    steps = len(f"{opcode:04d}")
    modes = get_modes(opcode)
    opcode = int(str(opcode)[-2:])
    if opcode in [1, 2, 7, 8]:
        first, second, third = get_values(intcode, position, modes)
        value, adress = OPCODE_TO_FUNCTION[opcode](first, second, third)
        # print(modes)
        return adress, value, position + steps
    elif opcode in [3, 4]:
        steps = 2
        adress = intcode[position + 1]
        if opcode == 3:
            return adress, inputs.pop(0), position + steps
        else:
            # opcode 4
            output.append(intcode[adress])
            return None, None, position + steps
    elif opcode in [5, 6]:
        steps = 3
        first, second, third = get_values(intcode, position, modes)
        # print(opcode, first, second, third)
        if opcode == 5 and first != 0:
            position = second
            return None, None, position
        if opcode == 6 and first == 0:
            position = second
            return None, None, position
        return None, None, position + steps

    else:
        # print(intcode[position])
        raise ValueError(f"Opcode {opcode} is not in {1, 2, 3, 4}")


# read input intcode
with open("input.txt") as file:
    intcode_start = file.read().rstrip("\n").split(",")
    intcode_start = [int(code) for code in intcode_start]


def process_intcode(intcode: Intcode, inputs: List[int]) -> DiagnosticCode:
    # process code
    position = 0
    while position < len(intcode):
        # print(intcode[:30])
        opcode = intcode[position]
        if opcode == 99:
            return output[-1]
            break
        # print(f"Evaluate: Position={position}, Opcode={opcode}")
        adress, value, position = evaluate_opcode(
            opcode, intcode, position, inputs
        )
        # print(f"Result: Adress={adress}, Value={value}, Position={position}")
        # print(f"Next Code: {intcode[position]}")
        if adress is not None:
            intcode[adress] = value
            # print(f"Value at {adress} was set to {value}")
            # print(f"{intcode[adress]}")
        # position += steps
        # if position > 300:
        #     break
    return intcode[0]


OPCODE_TO_FUNCTION = {
    1: add_next_values,
    2: multiply_next_values,
    7: less_than,
    8: equals,
}


NUMBER_TO_MODE = {
    0: Mode.POSITION,
    1: Mode.IMMEDIATE,
}


if __name__ == "__main__":

    amplifier_phases = [0, 1, 2, 3, 4]
    possible_phase_settings = itertools.permutations(amplifier_phases)
    output_signals = []

    for phase_setting in possible_phase_settings:
        second_input = 0
        for phase in phase_setting:
            inputs = [phase, second_input]
            output = []
            output_signal = process_intcode(intcode_start, inputs)
            second_input = output_signal

        output_signals.append(output_signal)

    print(f"Highest output signal is {max(output_signals)}")
