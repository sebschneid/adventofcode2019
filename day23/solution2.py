import enum
from typing import Dict, List, NamedTuple, NewType, Optional

import intcode
import network
from network import Adress


def solve(inputs):
    pass


TEST_INPUT = None
TEST_RESULT = None


if __name__ == "__main__":
    with open("input.txt") as file:
        intcode_string = file.read()
        intcode_start = intcode.get_intcode_from_input(intcode_string)

    # init 50 computers for network
    computers = {}
    for adress in range(50):
        program = intcode.Program(
            intcode_start.copy(), inputs=[adress], outputs=[]
        )
        output = program.run_to_next_input()
        program.clear_output()

        computers[Adress(adress)] = network.NetworkController(
            program=program, adress=Adress(adress), queue=[]
        )

    # init NatMonitor
    program = intcode.Program(intcode_start.copy(), inputs=[adress], outputs=[])
    computers[Adress(255)] = network.NatMonitor(program)

    # init network
    test_network = network.Network(computers)

    # solve until desired message is found
    first_message = None
    solved = False
    while not solved:
        for adress, computer in test_network.computers.items():
            if adress == Adress(255):
                # monitor network state. send when idle and check send packet against previous packet
                state = test_network.monitor_state()
                if state == network.NetworkState.IDLE:
                    messages = test_network.send(Adress(255), listen=True)
                    if messages:
                        second_message = messages[0]
                        if first_message:
                            if (
                                second_message.packet.y
                                == first_message.packet.y
                            ):
                                print(
                                    f"First Y value delivered twice by NAT to adress 0 is {second_message.packet.y}"
                                )
                                solved = True
                        first_message = second_message
            else:
                received = computer.receive()
                messages = test_network.send(adress, listen=True)
