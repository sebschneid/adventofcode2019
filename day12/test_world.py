import pytest

import world


TEST_INPUT_ONE = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""


TEST_INPUT_TwO = """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""


@pytest.mark.parametrize(
    "test_input,steps,total_energy",
    [(TEST_INPUT_ONE, 10, 179), (TEST_INPUT_TwO, 100, 1940)]
)
def test_total_energy_after_n_steps(test_input, steps, total_energy):
    test_world = world.world_from_inputs(test_input)
    test_world.simulate_steps(steps)
    assert test_world.get_total_energy() == total_energy
