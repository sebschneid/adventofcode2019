import logging

import intcode

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("run main")
    with open("input.txt") as file:
        intcode_string = file.read()
        intcode_start = intcode.get_intcode_from_input(intcode_string)

    TEST_INPUT = [1]
    program = intcode.Program(intcode_start, inputs=TEST_INPUT, outputs=[])
    output = program.run()

    logging.info(f"Finished! The BOOST keycode is {output[0]}")
