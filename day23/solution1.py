from typing import Dict, List, NamedTuple, NewType, Optional

import intcode
import network


if __name__ == "__main__":
    with open("input.txt") as file:
        intcode_string = file.read()
        intcode_start = intcode.get_intcode_from_input(intcode_string)

    computers = {}
    for adress in range(50):
        program = intcode.Program(
            intcode_start.copy(), inputs=[adress], outputs=[]
        )
        output = program.run_to_next_input()
        program.clear_output()

        computers[network.Adress(adress)] = network.NetworkController(
            program=program, adress=network.Adress(adress), queue=[]
        )

    program = intcode.Program(intcode_start.copy(), inputs=[adress], outputs=[])
    computers[network.Adress(255)] = network.NatMonitor(program)

    test_network = network.Network(computers)

    solved = False
    while not solved:
        for adress, computer in test_network.computers.items():
            computer.receive()
            if adress != network.Adress(255):
                messages = test_network.send(adress, listen=True)
            if messages:
                for message in messages:
                    if message.adress == 255:
                        print(
                            f"Y value of the first message sent to adreess 255 is {message.packet.y}"
                        )
                        solved = True
