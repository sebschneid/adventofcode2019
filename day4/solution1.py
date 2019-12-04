puzzle_input_string = "356261-846303"
puzzle_input = (356261, 846303)

count_passwords = 0

for number in range(*puzzle_input):
    number_string = str(number)
    digits = [digit for digit in number_string]
    ascending_order = sorted(digits) == digits
    adjacent_match = len(set(digits)) != len(digits)
    if ascending_order and adjacent_match:
        count_passwords += 1

print(f"There are {count_passwords} possible passwords in the input range!")
