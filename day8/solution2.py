import enum
import numpy as np

with open("input.txt") as file:
    image_digits = np.array(list(file.read().strip()), dtype=int)


width = 25
height = 6
layer_size = width * height
layers_count = image_digits.shape[0] // layer_size
image = image_digits.reshape(layers_count, height, width)

final_image = np.array(
    [
        [image[np.where(image[:, h, w] != 2)[0][0], h, w] for w in range(width)]
        for h in range(height)
    ]
)
print(final_image)
