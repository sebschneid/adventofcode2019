import numpy as np

with open("input.txt") as file:
    image_digits = np.array(list(file.read().strip()), dtype=int)

width = 25
height = 6
layer_size = width * height
layers_count = image_digits.shape[0] // layer_size

image = image_digits.reshape(layers_count, height, width)
zero_counts = (image == 0).sum(axis=1).sum(axis=1)
minimal_zero_layer = image[np.argmin(zero_counts)]
one_count = (minimal_zero_layer == 1).sum()
two_count = (minimal_zero_layer == 2).sum()

print(
    f"Count of ones times count of twos in the layer with least zeros is {one_count * two_count}"
)
