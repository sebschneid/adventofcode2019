import logging

import intcode


def test_copy():
    logging.debug(" TEST COPY")
    TEST_COPY = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    program = intcode.Program(intcode.get_intcode_from_input(TEST_COPY), inputs=[], outputs=[])
    output = program.run()
    result = [str(code) for code in output]
    assert ",".join(result) == TEST_COPY


def test_digits():
    logging.debug(" TEST DIGITS")
    TEST_DIGITS = "1102,34915192,34915192,7,4,7,99,0"
    program = intcode.Program(intcode.get_intcode_from_input(TEST_DIGITS), inputs=[], outputs=[])
    output = program.run()
    result = output[0]
    assert len(str(result)) == 16


def test_large_number():
    logging.debug(" TEST LARGE")
    TEST_OUTPUT_LARGE = "104,1125899906842624,99"
    program = intcode.Program(
        intcode.get_intcode_from_input(TEST_OUTPUT_LARGE), inputs=[], outputs=[]
    )
    output = program.run()
    result = output[0]
    assert result == 1125899906842624
