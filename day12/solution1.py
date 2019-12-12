import world

if __name__ == '__main__':
    with open("input.txt") as file:
        simulated_world = world.world_from_inputs(file.read())

    simulated_world.print()
    simulated_world.simulate_steps(1000)
    energy = simulated_world.get_total_energy()
    print(f"Total energy after 1000 steps is {energy}")

    #result = solve(inputs)