import logging

import asteroids

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    with open("input.txt") as file:
        inputs = file.read()

    asteroid_map = asteroids.asteroid_map_from_inputs(inputs)
    position, count = asteroids.asteroid_with_max_visible_asteroids(
        asteroid_map
    )
    position_of_200th = asteroids.nth_asteroid_destroyed(
        asteroid_map, position, 200
    )
    logging.info(
        f"X times 100 + Y coordinate of 200th destroyed asteroid ({position_of_200th}) "
        f"is {position_of_200th.x * 100 + position_of_200th.y}"
    )
