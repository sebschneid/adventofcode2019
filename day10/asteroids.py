import math
import enum
import logging
import operator
from typing import Dict, NamedTuple, NewType, Set, Tuple


class Position(NamedTuple):
    x: int
    y: int


class DistanceVector(NamedTuple):
    dx: int
    dy: int


class StepVector(DistanceVector):
    dx: int
    dy: int


class AsteroidMap(NamedTuple):
    asteroids: Dict[Position, int]
    size: Tuple[int, int]


def distance_vector(
    position_from: Position, position_to: Position
) -> DistanceVector:
    dx = position_to.x - position_from.x
    dy = position_to.y - position_from.y
    return DistanceVector(dx, dy)


def step_vector(vector: DistanceVector) -> StepVector:
    divisor = math.gcd(vector.dx, vector.dy)
    return StepVector(vector.dx // divisor, vector.dy // divisor)


def get_blocked_asteroids(
    position: Position, other_position: Position, asteroid_map: AsteroidMap
) -> Set[Position]:
    logging.debug(f"\n\nEvaluating other asteroid at position {other_position}")

    distance = distance_vector(position, other_position)
    step = step_vector(distance)

    logging.debug(f"DistanceVector is {distance}")
    logging.debug(f"StepVector is {step}")

    other_position = next_position(other_position, step)

    # add blocked asteroids
    blocked_asteroids = set()
    while position_in_map(other_position, asteroid_map):
        if other_position in list(asteroid_map.asteroids.keys()):
            logging.debug(f"Hidden asteroid at position {other_position}")
            blocked_asteroids.add(other_position)
        other_position = next_position(other_position, step)

    return blocked_asteroids


def next_position(position: Position, step: StepVector) -> Position:
    return Position(position.x + step.dx, position.y + step.dy)


def position_in_map(position: Position, asteroid_map: AsteroidMap) -> bool:
    return (position.x < asteroid_map.size[0] and position.x >= 0) and (
        position.y < asteroid_map.size[1] and position.y >= 0
    )


def asteroid_count(position: Position, asteroid_map: AsteroidMap) -> int:
    all_asteroid_positions = list(asteroid_map.asteroids.keys())
    other_asteroid_positions = set(all_asteroid_positions) - set([position])

    blocked_asteroids_all = set()
    for other_position in other_asteroid_positions:
        blocked_asteroids = get_blocked_asteroids(
            position, other_position, asteroid_map
        )
        blocked_asteroids_all = blocked_asteroids_all.union(blocked_asteroids)

        logging.debug(
            f"Finished for this asteroid. Asteroids at {blocked_asteroids} are not in sight"
        )

    asteroid_count = len(other_asteroid_positions - blocked_asteroids_all)
    logging.debug(
        f"For asteroid at position {position} the postions {blocked_asteroids_all} are not in sight, so {asteroid_count} are in sight!"
    )
    return asteroid_count


ASTEROID = "#"
FREE = "."


def asteroid_map_from_inputs(inputs: str) -> AsteroidMap:
    lines = inputs.split()
    asteroids = {}

    for y, line in enumerate(lines):
        for x, space in enumerate(line):
            if space == ASTEROID:
                asteroids[Position(x, y)] = 1

    x_size = len(lines[0])
    y_size = len(lines)
    asteroid_map = AsteroidMap(
        asteroids=asteroids, size=(x_size, y_size)
    )
    return asteroid_map


def asteroid_with_max_visible_asteroids(
    asteroid_map: AsteroidMap,
) -> Tuple[Position, int]:
    asteroid_to_count = {}
    for position in asteroid_map.asteroids.keys():
        logging.debug(f"Evaluating asteroid at position {position}")
        asteroid_to_count[position] = asteroid_count(position, asteroid_map)
        logging.debug(
            f"There are {asteroid_to_count[position]} asteroids in sight from this position!"
        )

    asteroid_position, max_count = max(
        asteroid_to_count.items(), key=operator.itemgetter(1)
    )
    logging.debug(
        f"Maximal asteroids visible from position {asteroid_position}: {max_count}"
    )
    return asteroid_position, max_count
