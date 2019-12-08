import time
import functools
from typing import NewType, Dict

import numpy as np


WorldObject = NewType("WorldObject", str)


def count_orbits(
    world_object: WorldObject, orbit_to_object: Dict[WorldObject, WorldObject]
):
    if world_object not in orbit_to_object.keys():
        return 0
    return 1 + count_orbits(orbit_to_object[world_object], orbit_to_object)


if __name__ == "__main__":
    time_start = time.time()
    with open("input.txt") as file:
        orbits = file.read().strip().split("\n")

    orbits_splitted = (entry.split(")") for entry in orbits)
    orbit_to_object = {
        WorldObject(b): WorldObject(a) for (a, b) in orbits_splitted
    }

    number_of_orbits = sum(
        count_orbits(world_object, orbit_to_object)
        for world_object in orbit_to_object.keys()
    )
    time_end = time.time()

    print(f"Total number of direct and indirect orbits is {number_of_orbits}")
    print(f"Solution took {time_end - time_start} seconds.")
