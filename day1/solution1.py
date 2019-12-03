# Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

import numpy as np

with open("input.txt") as file:
    module_masses = np.array(file.read().splitlines(), dtype=int)

fuels_required = np.floor(module_masses / 3) - 2

print(fuels_required.sum())