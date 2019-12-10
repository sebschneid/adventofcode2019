import logging

import asteroids

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    with open("input.txt") as file:
        inputs = file.read()

    asteroid_map = asteroids.asteroid_map_from_inputs(inputs)
    position, count = asteroids.asteroid_with_max_visible_asteroids(asteroid_map)
    logging.info(
        f"Asteroid at position {position} is best location for new monitoring"
        f" station with {count} detectable asteroids."
    )
