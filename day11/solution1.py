import logging

import intcode
import panel

logging.basicConfig(level=logging.DEBUG)


def solve(inputs):
    pass


TEST_INPUT = None
TEST_RESULT = None

assert solve(TEST_INPUT) == TEST_RESULT

if __name__ == "__main__":
    logging.info("run main")
    with open("input.txt") as file:
        intcode_string = file.read()
        intcode_start = intcode.get_intcode_from_input(intcode_string)

    TEST_INPUT = [0]
    program = intcode.Program(intcode_start, inputs=TEST_INPUT, outputs=[])
    panel_result, panel_count = program.run_with_robot()

    print(f"The robot painted {len(panel_count)} paanels at least one time!")
