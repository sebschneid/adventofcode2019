from wire import get_instructions, execute_instructions

with open("input.txt") as file:
    wire1_instruction_strings = file.readline().strip("\n").split(",")
    wire2_instruction_strings = file.readline().strip("\n").split(",")

wire1_instructions = get_instructions(wire1_instruction_strings)
wire2_instructions = get_instructions(wire2_instruction_strings)


positions1, _ = execute_instructions(wire1_instructions)
positions2, _ = execute_instructions(wire2_instructions)

intersection_points = positions1.intersection(positions2)
distances = [
    abs(position.x) + abs(position.y) for position in intersection_points
]

print(f"Minimal Manhattan Distance for intersection points is {min(distances)}")
