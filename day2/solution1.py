# 99: stop
# 1: add from two positions and store in third (next three integers)
# 2: like 1 but multiply
# Next opcode 4 positions later
'''
replace position 1 with the value 12 and replace position 2 with the value 2. What value is left at position 0 after the program halts?
'''


def evaluate_opcode(opcode, intcode, position):
    first_position = intcode[position + 1]
    second_position = intcode[position + 2]
    if opcode == 1:
        return intcode[first_position] + intcode[second_position]
    return intcode[first_position] * intcode[second_position]


# read input intcode
with open("input.txt") as file:
    intcode_start = file.read().rstrip("\n").split(',')
    intcode_start = [int(code) for code in intcode_start]


def process_intcode(noun, verb):
    intcode = intcode_start.copy()
    # init
    intcode[1] = noun
    intcode[2] = verb

    # process code
    position = 0
    while position < len(intcode):
        opcode = intcode[position]
        if opcode == 1 or opcode == 2:
            value = evaluate_opcode(opcode, intcode, position)
            intcode[intcode[position + 3]] = value
        else:
            break
        position += 4

    return intcode[0]


solution = 19690720

for noun in range(100):
    for verb in range(100):
        if process_intcode(noun, verb) == 19690720:
            print(noun, verb)
            print(f"Solution is {100 * noun + verb}.")
            break
