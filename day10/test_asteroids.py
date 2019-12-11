import copy
import math

import asteroids


def test_result(
    test_input: str, test_position: asteroids.Position, test_count: int
):
    asteroid_map = asteroids.asteroid_map_from_inputs(test_input)
    position, count = asteroids.asteroid_with_max_visible_asteroids(
        asteroid_map
    )
    assert position == test_position
    assert count == test_count


# test part 1


TEST_INPUT = """
.#..#
.....
#####
....#
...##
"""
test_result(TEST_INPUT, asteroids.Position(3, 4), 8)


TEST_INPUT = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""
test_result(TEST_INPUT, asteroids.Position(5, 8), 33)

TEST_INPUT = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""
test_result(TEST_INPUT, asteroids.Position(1, 2), 35)


TEST_INPUT = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""
test_result(TEST_INPUT, asteroids.Position(6, 3), 41)

TEST_INPUT = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
test_result(TEST_INPUT, asteroids.Position(11, 13), 210)


"""
Test for part 2
The 1st asteroid to be vaporized is at 11,12.
The 2nd asteroid to be vaporized is at 12,1.
The 3rd asteroid to be vaporized is at 12,2.
The 10th asteroid to be vaporized is at 12,8.
The 20th asteroid to be vaporized is at 16,0.
The 50th asteroid to be vaporized is at 16,9.
The 100th asteroid to be vaporized is at 10,16.
The 199th asteroid to be vaporized is at 9,6.
The 200th asteroid to be vaporized is at 8,2.
The 201st asteroid to be vaporized is at 10,9.
The 299th and final asteroid to be vaporized is at 11,1.
"""
TEST_INPUT = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
asteroid_map = asteroids.asteroid_map_from_inputs(TEST_INPUT)
position, count = asteroids.asteroid_with_max_visible_asteroids(asteroid_map)

assert asteroids.Position(11, 12) == asteroids.nth_asteroid_destroyed(
    copy.deepcopy(asteroid_map), position, 1
)
assert asteroids.Position(12, 1) == asteroids.nth_asteroid_destroyed(
    copy.deepcopy(asteroid_map), position, 2
)
assert asteroids.Position(12, 2) == asteroids.nth_asteroid_destroyed(
    copy.deepcopy(asteroid_map), position, 3
)
assert asteroids.Position(12, 8) == asteroids.nth_asteroid_destroyed(
    copy.deepcopy(asteroid_map), position, 10
)
assert asteroids.Position(16, 0) == asteroids.nth_asteroid_destroyed(
    copy.deepcopy(asteroid_map), position, 20
)
assert asteroids.Position(16, 9) == asteroids.nth_asteroid_destroyed(
    copy.deepcopy(asteroid_map), position, 50
)
assert asteroids.Position(10, 16) == asteroids.nth_asteroid_destroyed(
    copy.deepcopy(asteroid_map), position, 100
)
assert asteroids.Position(9, 6) == asteroids.nth_asteroid_destroyed(
    copy.deepcopy(asteroid_map), position, 199
)
assert asteroids.Position(8, 2) == asteroids.nth_asteroid_destroyed(
    copy.deepcopy(asteroid_map), position, 200
)
assert asteroids.Position(10, 9) == asteroids.nth_asteroid_destroyed(
    copy.deepcopy(asteroid_map), position, 201
)
assert asteroids.Position(11, 1) == asteroids.nth_asteroid_destroyed(
    copy.deepcopy(asteroid_map), position, 299
)
