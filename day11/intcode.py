import collections
import enum
from typing import Dict, List, NamedTuple, Optional, Tuple
import logging

import panel

logging.basicConfig(level=logging.INFO)


def add_next_values(first, second):
    return first + second


def multiply_next_values(first, second):
    return first * second


def less_than(first, second):
    if first < second:
        return 1
    return 0


def equals(first, second):
    if first == second:
        return 1
    return 0


class Program:
    position: int
    intcode: Dict[int, int]
    relative_base: int
    inputs: List[int]
    outputs: List[int]

    def __init__(
        self,
        intcode: Dict[int, int],
        position: int = 0,
        relative_base: int = 0,
        inputs: List[int] = [],
        outputs: List[int] = [],
    ):
        self.intcode = intcode
        self.position = position
        self.relative_base = relative_base
        self.inputs = inputs
        self.outputs = outputs

    def log_status(self):
        logging.debug(
            f"Position: {self.position},"
            f"Relative_base: {self.relative_base}, "
            f"Opcode at Postion: {self.intcode[self.position]}, "
            f"Outputs: {self.outputs}, "
            f"Inputs: {self.inputs}"
        )

    def run(self) -> List[Optional[int]]:
        while True:
            self.log_status()
            opcode = self.intcode[self.position]

            if opcode == 99:
                return self.outputs
            self.evaluate_opcode(opcode)

        return self.outputs

    def run_with_robot(
        self,
        panel_position: panel.PanelPosition = panel.PanelPosition(0, 0),
        direction: panel.StepVector = panel.StepVector(0, 1),
    ) -> Tuple[panel.Panel, panel.PanelCount]:
        self.panel: panel.Panel = {}
        self.panel_count: panel.PanelCount = collections.defaultdict(int)
        self.panel_position = panel_position
        self.robot_direction = direction

        while True:
            self.log_status()
            opcode = self.intcode[self.position]

            if opcode == 99:
                return self.panel, self.panel_count

            self.evaluate_opcode(opcode)
            if len(self.outputs) == 2:
                # get robot instruction from outputs
                logging.debug(f"Instructions for robot: {self.outputs}")
                logging.debug(
                    f"Robot is at {self.panel_position} in direction {self.robot_direction}"
                )
                color, rotation = self.outputs

                # paint panel to color by instruction and increment count
                logging.debug(f"Robot paints {panel.OUTPUT_TO_COLOR[color]}")
                self.panel[self.panel_position] = panel.OUTPUT_TO_COLOR[color]
                self.panel_count[self.panel_position] += 1
                logging.debug(
                    f"Robot painted {self.panel_count[self.panel_position]} times at {self.panel_position}"
                )

                # turn left / right with robot
                logging.debug(
                    f"Robot turns {panel.OUTPUT_TO_ROTATION[rotation]}"
                )
                self.robot_direction = panel.rotate_vector(
                    self.robot_direction, panel.OUTPUT_TO_ROTATION[rotation]
                )
                logging.debug(
                    f"Robot's new direction is {self.robot_direction}."
                )

                # move one step
                self.panel_position = panel.next_position(
                    self.panel_position, self.robot_direction
                )
                self.inputs.append(
                    panel.COLOR_TO_INPUT[
                        self.panel.get(self.panel_position, panel.Color.BLACK)
                    ]
                )
                logging.debug(f"Robot moved to {self.panel_position}")
                logging.debug(
                    f"Color at this position is {self.panel.get(self.panel_position, panel.Color.BLACK)}"
                )

                # reset output and get new input from color
                self.outputs = []
                logging.debug(f"Current input for Intcode is {self.inputs}")

    def evaluate_opcode(self, opcode):
        modes = get_modes(opcode)
        opcode = int(str(opcode)[-2:])
        if opcode in [1, 2, 7, 8]:
            first_parameter = self.use_read_mode(1, modes[0])
            second_parameter = self.use_read_mode(2, modes[1])
            result = OPCODE_TO_FUNCTION[opcode](
                first_parameter, second_parameter
            )
            self.use_write_mode(3, result, modes[2])
            self.position += 4

        elif opcode in [3, 4]:
            if opcode == 3:
                self.use_write_mode(1, self.inputs.pop(0), modes[0])
            if opcode == 4:
                logging.debug(f"Opcode 4: Mode is {modes[0]}")
                value = self.use_read_mode(1, modes[0])
                self.outputs.append(value)
            self.position += 2

        elif opcode in [5, 6]:
            first_parameter = self.use_read_mode(1, modes[0])
            second_parameter = self.use_read_mode(2, modes[1])
            logging.debug(
                f"First: {first_parameter}, Second: {second_parameter}"
            )

            if opcode == 5 and first_parameter != 0:
                self.position = second_parameter
            elif opcode == 6 and first_parameter == 0:
                self.position = second_parameter
            else:
                self.position += 3

        elif opcode == 9:
            first_parameter = self.use_read_mode(1, modes[0])
            self.relative_base += first_parameter
            self.position += 2

    def use_read_mode(self, position_offset, mode):
        if mode == Mode.POSITION:
            return self.intcode.get(
                self.intcode.get(self.position + position_offset, 0), 0
            )
        if mode == Mode.IMMEDIATE:
            return self.intcode.get(self.position + position_offset, 0)
        if mode == Mode.RELATIVE:
            return self.intcode.get(
                self.intcode.get(self.position + position_offset, 0)
                + self.relative_base,
                0,
            )

    def use_write_mode(self, position_offset, value, mode):
        if mode == Mode.POSITION:
            self.intcode[
                self.intcode.get(self.position + position_offset, 0)
            ] = value
        if mode == Mode.IMMEDIATE:
            raise ValueError(
                "IMMEDIATE mode not possible for write instructions!"
            )
        if mode == Mode.RELATIVE:
            self.intcode[
                self.intcode.get(self.position + position_offset, 0)
                + self.relative_base
            ] = value


def get_intcode_from_input(intcode_string):
    return {
        pos: int(code)
        for pos, code in enumerate(intcode_string.rstrip("\n").split(","))
    }


class Mode(enum.Enum):
    POSITION = enum.auto()
    IMMEDIATE = enum.auto()
    RELATIVE = enum.auto()


def get_modes(opcode):
    first_mode = NUMBER_TO_MODE[opcode // 100 % 10]
    second_mode = NUMBER_TO_MODE[opcode // 1000 % 10]
    third_mode = NUMBER_TO_MODE[opcode // 10000 % 10]
    # write mode is never IMMEDIATE
    return (first_mode, second_mode, third_mode)


OPCODE_TO_FUNCTION = {
    1: add_next_values,
    2: multiply_next_values,
    7: less_than,
    8: equals,
}


NUMBER_TO_MODE = {
    0: Mode.POSITION,
    1: Mode.IMMEDIATE,
    2: Mode.RELATIVE,
}

# TESTING
logging.debug(" TEST COPY")
TEST_COPY = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
program = Program(get_intcode_from_input(TEST_COPY), inputs=[], outputs=[])
output = program.run()
result = [str(code) for code in output]
assert ",".join(result) == TEST_COPY


logging.debug(" TEST DIGITS")
TEST_DIGITS = "1102,34915192,34915192,7,4,7,99,0"
program = Program(get_intcode_from_input(TEST_DIGITS), inputs=[], outputs=[])
output = program.run()
result = output[0]
assert len(str(result)) == 16


logging.debug(" TEST LARGE")
TEST_OUTPUT_LARGE = "104,1125899906842624,99"
program = Program(
    get_intcode_from_input(TEST_OUTPUT_LARGE), inputs=[], outputs=[]
)
output = program.run()
result = output[0]
assert result == 1125899906842624
