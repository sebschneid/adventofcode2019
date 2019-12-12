
import logging
from typing import Dict, List, NamedTuple, Tuple, Set, NewType
import itertools

import numpy as np

logging.basicConfig(level=logging.INFO)


Position = NewType("Position", Dict[str, int])
Velocity = NewType("Velocity", Dict[str, int])


AXES = ['x', 'y', 'z']


class Moon(NamedTuple):
    pos: Position
    vel: Velocity


Moons = List[Moon]


class World:
    moons: Moons
    time: int

    def __init__(self, moons: Moons):
        self.moons = moons
        self.time = 0

    def print(self):
        print(f"Time: {self.time}")
        for i, moon in enumerate(self.moons):
            print(f"Moon {i} - Position: {moon.pos} Velocity: {moon.vel}")

    def log_moons(self) -> None:
        for i, moon in enumerate(self.moons):
            logging.debug(f"Moon {i} - Position: {moon.pos} Velocity: {moon.vel}")

    def simulate_steps(self, steps: int) -> None:
        for _ in range(steps):
            self.step()

    def step(self) -> None:
        logging.debug("Take on step in time!")
        self.update_velocity()
        self.update_position()
        self.time += 1
        logging.debug("New moons are:")
        self.log_moons()

    def update_velocity(self) -> None:
        pair_of_moons = itertools.combinations(self.moons, 2)
        for pair in pair_of_moons:
            apply_gravity(*pair)

    def update_position(self) -> None:
        for moon in self.moons:
            apply_velocity(moon)

    def get_total_energy(self) -> int:
        return sum([total_energy(moon) for moon in self.moons])


def apply_gravity_on_axes(moon1: Moon, moon2: Moon, axis: str) -> int:
    return np.sign(moon2.pos[axis] - moon1.pos[axis])


def apply_gravity(moon1: Moon, moon2: Moon) -> None:
    logging.debug(f"\nApply gravity!")
    logging.debug(f"Moon1 - Position: {moon1.pos} Velocity: {moon1.vel}")
    logging.debug(f"Moon2 - Position: {moon2.pos} Velocity: {moon2.vel}")
    for axis in AXES:
        moon1.vel[axis] += apply_gravity_on_axes(moon1, moon2, axis)
        moon2.vel[axis] += apply_gravity_on_axes(moon2, moon1, axis)
    logging.debug(f"Velocities changed!")
    logging.debug(f"Moon1 - Position: {moon1.pos} Velocity: {moon1.vel}")
    logging.debug(f"Moon2 - Position: {moon2.pos} Velocity: {moon2.vel}")


def apply_velocity(moon: Moon) -> None:
    logging.debug(f"\nApply velocity!")
    logging.debug(f"Moon - Position: {moon.pos} Velocity: {moon.vel}")
    for axis in AXES:
        moon.pos[axis] += moon.vel[axis]
    logging.debug(f"Positions changed!")
    logging.debug(f"Moon - Position: {moon.pos} Velocity: {moon.vel}")


def total_energy(moon: Moon) -> int:
    return kinetic_energy(moon) * potential_energy(moon)


def kinetic_energy(moon: Moon) -> int:
    return sum([abs(vel) for vel in moon.vel.values()])


def potential_energy(moon: Moon) -> int:
    return sum([abs(pos) for pos in moon.pos.values()])


def parse_position(line):
    assignments = line.split("=")[1:]
    positions = [int(a.strip(">").split(",")[0]) for a in assignments]
    return Position({axis: pos for axis, pos in zip(AXES, positions)})


def world_from_inputs(inputs: str) -> World:
    lines = inputs.strip().split("\n")
    moons = [Moon(parse_position(line), Velocity({axis: 0 for axis in AXES})) for line in lines]
    return World(moons)
