import enum
from typing import Dict, NamedTuple


class Color(enum.Enum):
    BLACK = "."
    WHITE = "#"


class Rotation(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()


class Position(NamedTuple):
    x: int
    y: int


class PanelPosition(Position):
    x: int
    y: int


class DistanceVector(NamedTuple):
    dx: int
    dy: int


class StepVector(DistanceVector):
    dx: int
    dy: int


Panel = Dict[PanelPosition, Color]
PanelCount = Dict[PanelPosition, int]


OUTPUT_TO_COLOR = {
    0: Color.BLACK,
    1: Color.WHITE,
}

OUTPUT_TO_ROTATION = {0: Rotation.LEFT, 1: Rotation.RIGHT}

COLOR_TO_INPUT = {
    Color.BLACK: 0,
    Color.WHITE: 1,
}


def next_position(position: Position, step: StepVector) -> Position:
    return Position(position.x + step.dx, position.y + step.dy)


def rotate_vector(vector: StepVector, rotation: Rotation) -> StepVector:
    # x' = cos(phi) x - sin(phi) y
    # y' = sin(phi) x + cos(phi) x
    if rotation == Rotation.LEFT:
        return StepVector(dx=-vector.dy, dy=vector.dx)
    elif rotation == Rotation.RIGHT:
        return StepVector(dx=vector.dy, dy=-vector.dx)
    else:
        raise ValueError("Rotation not one of {LEFT, RIGHT}")
