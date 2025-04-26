import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
import numpy as np
from skimage.color import rgb2hsv

image = plt.imread("balls_and_rects.png")

hsv_image = rgb2hsv(image)

gray = image.mean(axis=2)
binary = gray > 0

labeled = label(binary)
regions = regionprops(labeled)

sq = 0
ci = 0
count = 0

colors_sq = []
colors_ci = []
colors_full = []

for region in regions:
    y, x = region.centroid
    color = (hsv_image[int(y), int(x), 0])
    if region.extent < 1:
        colors_ci.append(hsv_image[int(y), int(x), 0])
        ci += 1
    else:
        colors_sq.append(hsv_image[int(y), int(x), 0])
        sq += 1
    count += 1
    colors_full.append(hsv_image[int(y), int(x), 0])

def colors(shades, count):
    d = (np.diff(sorted(shades)))
    pos = np.where(d > np.std(d) * 2)
    result = ""
    count_color = []
    pos_ = np.append(pos[0], count - 1)
    pos_ = np.append(0, pos_)
    for i in range(len(pos_) - 1):
        count_color.append(pos_[i + 1] - pos_[i])
        result += (f"\n\tКоличество с оттенком {i + 1} - {count_color[i]}")
    return result

print(f"Всего фигур - {count} \nПрямоугольников - {sq}, кругов - {ci} \nФигур по оттенкам - {colors(colors_full, count)} \nКоличество прямоугольников по оттенкам - {colors(colors_sq, sq)} \nКоличество кругов по оттенкам - {colors(colors_ci, ci)}")