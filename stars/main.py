import numpy as np
from skimage.measure import label
from skimage.morphology import binary_opening

image = np.load("stars.npy")

new_image = image.copy()

plus = np.array([
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
])

crosses = np.array([
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1]
])

new_image_plus = binary_opening(new_image, plus)
new_image_crosses = binary_opening(new_image, crosses)

print(f"Количество звездочек: {np.max(label(new_image_plus)) + np.max(label(new_image_crosses))}")