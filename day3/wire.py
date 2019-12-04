import enum
import numpy as np
from typing import NamedTuple, List, Set
import itertools


class Direction(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()


class Position(NamedTuple):
    x: int
    y: int


class Instruction(NamedTuple):
    direction: Direction
    steps: int


STRING_TO_DIRECTION = {
    "L": Direction.LEFT,
    "R": Direction.RIGHT,
    "U": Direction.UP,
    "D": Direction.DOWN,
}

DIRECTION_TO_MOVE = {
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
    Direction.UP: (0, 1),
    Direction.DOWN: (0, -1),
}


def get_instructions(instruction_strings: List[str]) -> List[Instruction]:
    return [
        Instruction(
            direction=STRING_TO_DIRECTION[string[0]], steps=int(string[1:])
        )
        for string in instruction_strings
    ]


def update_position(position: Position, direction: Direction) -> Position:
    new_x = position.x + DIRECTION_TO_MOVE[direction][0]
    new_y = position.y + DIRECTION_TO_MOVE[direction][1]
    return Position(x=new_x, y=new_y)


def execute_instructions(instructions: List[Instruction]) -> Set[Position]:
    current_position = Position(x=0, y=0)
    positions = set()
    positions_to_length = {}
    counter = 1
    for instruction in instructions:
        for step in range(instruction.steps):
            current_position = update_position(
                current_position, instruction.direction
            )
            positions.add(current_position)
            if current_position not in positions_to_length.keys():
                positions_to_length[current_position] = counter
            counter += 1
    return positions, positions_to_length
