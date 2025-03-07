import numpy as np
import matplotlib.pyplot as plt


external = np.diag([1, 1, 1, 1]).reshape(4, 2, 2)

internal = np.logical_not(external)

cross = np.array([[[1, 0], [0, 1]], [[0, 1], [1, 0]]])


def match(a, masks):
    for mask in masks:
        if np.all(a == mask):
            return True
    return False


def count_objects(image):
    E = 0
    for y in range(0, image.shape[0] - 1):
        for x in range(0, image.shape[1] - 1):
            sub = image[y : y + 2, x : x + 2]
            if match(sub, external):
                E += 1
            elif match(sub, internal):
                E -= 1
            elif match(sub, cross):
                E += 2
    return E / 4

def descritize(image):
    mn = image.min()
    result = image.copy()
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image.ndim == 2:
                if result[y, x] != mn:
                    result[y, x] = 1
            elif image.ndim == 3:
                if np.any(result[y, x] != mn):
                    result[y, x] = [1, 1, 1]

    return result

files = ["example1.npy", "example2.npy"]
for file in files:
    image = np.load(file)

    if image.ndim == 3:

        print(f"Total objects in {file}: {sum([count_objects(descritize(image[:, :, i])) for i in range(image.shape[2])])}")
        print(image.shape)
        plt.imshow((image))
        plt.show()

    elif image.ndim == 2:

        print(f"Total objects in {file}: {count_objects(descritize(image))}")
        plt.imshow(image)
        plt.show()