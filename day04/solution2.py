import time
import collections

import numpy as np

puzzle_input_string = "356261-846303"
puzzle_input = (356261, 846303)

time1 = time.time()
count_passwords = 0
for number in range(*puzzle_input):
    number_string = str(number)
    digits = [digit for digit in number_string]

    ascending_order = sorted(digits) == digits

    # numpy variant: 16s
    # unique, counts = np.unique(digits, return_counts=True)
    # adjacent_match_outside_larger_group = any(counts == 2)

    # colletions.Counter variant: 3s
    counts = collections.Counter(digits)
    adjacent_match_outside_larger_group = (
        len([count for count in counts.values() if count == 2]) > 0
    )

    if ascending_order and adjacent_match_outside_larger_group:
        count_passwords += 1

time2 = time.time()
print(f"Took {time2-time1} seconds")
print(f"There are {count_passwords} possible passwords in the input range!")
