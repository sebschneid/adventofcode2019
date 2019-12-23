import enum
import intcode
from typing import Dict, List, NamedTuple, NewType, Optional, Union

Adress = NewType("Adress", int)


class Packet(NamedTuple):
    x: int
    y: int


class Message(NamedTuple):
    adress: Adress
    packet: Packet


class NetworkController:
    program: intcode.Program
    adress: Adress
    queue: List[Packet]
    sending: bool
    receiving: bool

    def __init__(self, program, adress, queue) -> None:
        self.program = program
        self.adress = adress
        self.queue = queue

    def receive(self) -> None:
        if not self.queue:
            self.program.add_inputs(-1)
            self.receiving = False
        else:
            packet = self.queue.pop(0)
            self.program.add_inputs([packet.x, packet.y])
            self.receiving = True

    def send(self) -> Optional[List[Message]]:
        output = self.program.run_to_next_input()
        self.program.clear_output()
        messages = []
        if output:
            message_count = len(output) // 3
            for start in range(0, len(output), 3):
                adress, x, y = output[start : start + 3]
                messages.append(Message(Adress(adress), Packet(x, y)))
            self.sending = True
            return messages
        else:
            self.sending = False
            return None

    def add_packet(self, packet: Packet) -> None:
        self.queue.append(packet)


class NatMonitor(NetworkController):
    program: intcode.Program
    adress: Adress
    received_packet: Optional[Packet]

    def __init__(self, program) -> None:
        self.program = program
        self.adress = Adress(255)
        self.received_packet = None

    def receive(self) -> bool:
        if not self.received_packet:
            self.program.add_inputs(-1)
            return False
        else:
            self.program.clear_inputs()
            self.program.add_inputs(
                [self.received_packet.x, self.received_packet.y]
            )
            return True

    def send(self) -> List[Message]:
        return [
            Message(
                Adress(0),
                Packet(self.received_packet.x, self.received_packet.y),
            )
        ]

    def add_packet(self, packet: Packet) -> None:
        self.received_packet = packet


class NetworkState(enum.Enum):
    IDLE = enum.auto()
    RUNNING = enum.auto()


class Network:
    computers: Dict[Adress, NetworkController]

    def __init__(self, computers):
        self.computers = computers

    def send(
        self, from_adress: Adress, listen: bool = False
    ) -> Optional[List[Message]]:
        messages = self.computers[from_adress].send()
        if messages:
            for message in messages:
                self.computers[message.adress].add_packet(message.packet)
        if listen:
            return messages

    def monitor_state(self) -> NetworkState:
        if Adress(255) not in self.computers.keys():
            raise ValueError("Adress 255 is not setup to monitor the network!")

        sending = False
        receiving = False
        for adress, computer in self.computers.items():
            if adress != Adress(255):
                if computer.sending:
                    return NetworkState.RUNNING
                if computer.receiving:
                    return NetworkState.RUNNING

        return NetworkState.IDLE
