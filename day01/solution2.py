import numpy as np


def get_fule_for_module(module_mass):
    fuel_required = np.floor(module_mass / 3) - 2
    if fuel_required <= 0:
        return 0
    return fuel_required + get_fule_for_module(fuel_required)


with open("input.txt") as file:
    module_masses = np.array(file.read().splitlines(), dtype=int)

fuels_required = list(map(get_fule_for_module, module_masses))
print(sum(fuels_required))
