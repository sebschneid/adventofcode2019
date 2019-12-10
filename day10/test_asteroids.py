import asteroids


def test_position(test_input: str, test_result: asteroids.Position):
    asteroid_map = asteroids.asteroid_map_from_inputs(test_input)
    position, _ = asteroid_with_max_visible_asteroids.solve(asteroid_map)
    assert position == test_result


TEST_INPUT = """
.#..#
.....
#####
....#
...##
"""
test_position(TEST_INPUT, Position(3, 4))


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
test_position(TEST_INPUT, Position(5, 8))

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
test_position(TEST_INPUT, Position(1, 2))


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
test_position(TEST_INPUT, Position(6, 3))

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
test_position(TEST_INPUT, Position(11, 13))
