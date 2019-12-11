import logging

import numpy as np

import intcode
import panel

logging.basicConfig(level=logging.INFO)


def print_panel(panel_to_print: panel.Panel) -> None:
    x_min = min(panel_to_print.keys(), key=lambda pos: pos.x).x
    x_max = max(panel_to_print.keys(), key=lambda pos: pos.x).x
    y_min = min(panel_to_print.keys(), key=lambda pos: pos.y).y
    y_max = max(panel_to_print.keys(), key=lambda pos: pos.y).y

    x_size = x_max - x_min + 1
    y_size = y_max - y_min + 1
    x_shift = -x_min
    y_shift = y_min - 1

    panel_representation = [
        [panel.Color.BLACK.value for _ in range(x_size)] for _ in range(y_size)
    ]

    for pos, color in panel_to_print.items():
        panel_representation[-pos.y + y_shift][pos.x + x_shift] = color.value

    for row in panel_representation:
        print("".join(row))


if __name__ == "__main__":
    logging.info("run main")
    with open("input.txt") as file:
        intcode_string = file.read()
        intcode_start = intcode.get_intcode_from_input(intcode_string)

    TEST_INPUT = [1]
    program = intcode.Program(intcode_start, inputs=TEST_INPUT, outputs=[])
    panel_result, panel_count = program.run_with_robot()

    print("The message on the panel is:")
    print_panel(panel_result)
