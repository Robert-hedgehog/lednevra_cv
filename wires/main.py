import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import (binary_closing, binary_dilation, binary_erosion, binary_opening)

files = ["wires1npy.txt", "wires2npy.txt", "wires3npy.txt", "wires4npy.txt", "wires5npy.txt", "wires6npy.txt"]

for file in files:
    data = np.load(file)
    print(f"{file}")
    labeled = label(data) # маркируем изображение
    for i in range (1, np.max(labeled) + 1):

        result = binary_erosion(labeled == i, np.ones(3).reshape(3, 1)) # разделить на части

        porvan = np.max(label(result))
        if porvan > 1:
            print(f"Провод {i} порван на {porvan} части/частей")
        elif porvan == 1:
            print(f"Провод {i} цел")
        else:
            print(f"Провод {i} уничтожен")
        plt.figure()
        plt.subplot(121)
        plt.imshow(data)
        plt.subplot(122)
        plt.imshow(result)
    plt.show()