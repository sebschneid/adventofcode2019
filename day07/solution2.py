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
    first_mode = NUMBER_TO_MODE[opcode // 100 % 10]
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


def evaluate_opcode(
    opcode, intcode, position, inputs
):  # -> adress, value, new_position, output
    steps = len(f"{opcode:04d}")
    modes = get_modes(opcode)
    opcode = int(str(opcode)[-2:])
    if opcode in [1, 2, 7, 8]:
        first, second, third = get_values(intcode, position, modes)
        value, adress = OPCODE_TO_FUNCTION[opcode](first, second, third)
        return adress, value, position + steps, None
    elif opcode in [3, 4]:
        steps = 2
        adress = intcode[position + 1]
        if opcode == 3:
            return adress, inputs.pop(0), position + steps, None
        else:
            output_signal = intcode[adress]
            return None, None, position + steps, output_signal
    elif opcode in [5, 6]:
        steps = 3
        first, second, third = get_values(intcode, position, modes)
        if opcode == 5 and first != 0:
            position = second
            return None, None, position, None
        if opcode == 6 and first == 0:
            position = second
            return None, None, position, None
        return None, None, position + steps, None

    else:
        raise ValueError(f"Opcode {opcode} is not in {1, 2, 3, 4}")


def process_intcode(
    intcode: Intcode, position: int, inputs: List[int], outputs: List[int]
) -> DiagnosticCode:
    # process code
    while position < len(intcode):
        opcode = intcode[position]
        if opcode == 99:
            return outputs[-1], False, None, None, outputs
            break
        adress, value, position, output_signal = evaluate_opcode(
            opcode, intcode, position, inputs
        )
        if output_signal is not None:
            outputs.append(output_signal)
            return output_signal, True, intcode, position, outputs

        if adress is not None:
            intcode[adress] = value

    return intcode[0], False, None, None, outputs


def get_thruster_signal(intcode_start, phase_setting):
    amplifier_to_phase = {
        amplifier: phase for amplifier, phase in zip("ABCDE", phase_setting)
    }
    amplifier_continues = {amplifier: True for amplifier in "ABCDE"}
    amplififier_to_program = {
        amplifier: {
            "code": intcode_start.copy(),
            "position": 0,
            "inputs": [amplifier_to_phase[amplifier]],
            "outputs": [],
        }
        for amplifier in "ABCDE"
    }

    amplifier = "A"
    amplififier_to_program["A"]["inputs"].append(0)

    while True:
        current_intcode = amplififier_to_program[amplifier]["code"]
        current_position = amplififier_to_program[amplifier]["position"]
        current_inputs = amplififier_to_program[amplifier]["inputs"]
        current_outputs = amplififier_to_program[amplifier]["outputs"]

        (
            output_signal,
            continue_process,
            current_intcode,
            current_position,
            current_outputs,
        ) = process_intcode(
            current_intcode, current_position, current_inputs, current_outputs
        )

        if continue_process:
            amplififier_to_program[amplifier]["code"] = current_intcode
            amplififier_to_program[amplifier]["position"] = current_position
            amplififier_to_program[amplifier]["outputs"] = current_outputs

            amplifier = AMPLIFIER_CONNECTIONS[amplifier]
            amplififier_to_program[amplifier]["inputs"].append(output_signal)
            continue

        else:
            amplifier_continues[amplifier] = False
            amplifier = AMPLIFIER_CONNECTIONS[amplifier]
            amplififier_to_program[amplifier]["inputs"].append(output_signal)

        if not any(amplifier_continues.values()):
            return amplififier_to_program["E"]["outputs"][-1]


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

AMPLIFIER_CONNECTIONS = {
    "A": "B",
    "B": "C",
    "C": "D",
    "D": "E",
    "E": "A",
}


## TESTING
# TEST 1
test1 = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
intcode_test1 = [int(code) for code in test1.split(",")]
phase_setting_test1 = [9, 8, 7, 6, 5]
result_test1 = 139629729
assert get_thruster_signal(intcode_test1, phase_setting_test1) == result_test1

# TEST 2
test2 = (
    "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,"
    "-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,"
    "53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
)
intcode_test2 = [int(code) for code in test2.split(",")]
phase_setting_test2 = [9, 7, 8, 5, 6]
result_test2 = 18216
assert get_thruster_signal(intcode_test2, phase_setting_test2) == result_test2

## Main
if __name__ == "__main__":
    # read input intcode
    with open("input.txt") as file:
        intcode_start = file.read().rstrip("\n").split(",")
        intcode_start = [int(code) for code in intcode_start]

    amplifier_phases = [5, 6, 7, 8, 9]
    possible_phase_settings = itertools.permutations(amplifier_phases)
    output_signals = []
    for phase_setting in possible_phase_settings:
        output_signals.append(get_thruster_signal(intcode_start, phase_setting))

    print(f"Highest output signal is {max(output_signals)}")
