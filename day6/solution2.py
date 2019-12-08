import time
import numpy as np


def get_orbit(orbit):
    orbitted_object = object_to_orbitted_object.get(orbit, None)
    return (
        set([orbitted_object]).union(get_orbit(orbitted_object))
        if orbitted_object
        else set({})
    )


def count_orbits_to_destination(orbit, destination):
    # print(orbit, destination)
    if orbit == destination:
        return 0
    return 1 + count_orbits_to_destination(
        object_to_orbitted_object[orbit], destination
    )


if __name__ == "__main__":
    time_start = time.time()
    with open("input.txt") as file:
        orbits = file.read().strip().split("\n")

    object_to_orbitted_object = {
        entry.split(")")[1]: entry.split(")")[0] for entry in orbits
    }

    start_object = object_to_orbitted_object["YOU"]
    end_object = object_to_orbitted_object["SAN"]
    start_orbitting_objects = []

    start_orbits = get_orbit(start_object)
    end_orbits = get_orbit(end_object)
    common_objects = start_orbits.intersection(end_orbits)

    sums_to_destination = {}
    for common_object in common_objects:
        path_to_start = count_orbits_to_destination(start_object, common_object)
        path_to_end = count_orbits_to_destination(end_object, common_object)
        sums_to_destination[common_object] = path_to_end + path_to_start

    time_end = time.time()
    min_distance = min(sums_to_destination.values())
    print(f"Minimal path is {min_distance}")
    print(f"Solution took {time_end - time_start} seconds.")
