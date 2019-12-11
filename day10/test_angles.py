import math

import asteroids


def radians(degree):
    return degree / 360 * math.pi * 2


assert radians(0) == asteroids.get_angle(
    asteroids.clockwise_vector(
        asteroids.rotate_vector(asteroids.DistanceVector(0, 1))
    )
)
assert radians(45) == asteroids.get_angle(
    asteroids.clockwise_vector(
        asteroids.rotate_vector(asteroids.DistanceVector(1, 1))
    )
)
assert radians(90) == asteroids.get_angle(
    asteroids.clockwise_vector(
        asteroids.rotate_vector(asteroids.DistanceVector(1, 0))
    )
)
assert radians(135) == asteroids.get_angle(
    asteroids.clockwise_vector(
        asteroids.rotate_vector(asteroids.DistanceVector(1, -1))
    )
)
assert radians(180) == asteroids.get_angle(
    asteroids.clockwise_vector(
        asteroids.rotate_vector(asteroids.DistanceVector(0, -1))
    )
)
assert radians(225) == asteroids.get_angle(
    asteroids.clockwise_vector(
        asteroids.rotate_vector(asteroids.DistanceVector(-1, -1))
    )
)
assert radians(270) == asteroids.get_angle(
    asteroids.clockwise_vector(
        asteroids.rotate_vector(asteroids.DistanceVector(-1, 0))
    )
)
assert radians(315) == asteroids.get_angle(
    asteroids.clockwise_vector(
        asteroids.rotate_vector(asteroids.DistanceVector(-1, 1))
    )
)
