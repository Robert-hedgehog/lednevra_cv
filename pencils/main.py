import cv2
import numpy as np

files = ["img (1).jpg", "img (2).jpg", "img (3).jpg", "img (4).jpg", "img (5).jpg", "img (6).jpg", "img (7).jpg", "img (8).jpg", "img (9).jpg", "img (10).jpg", "img (11).jpg", "img (12).jpg"]
final = 0
for file in files:
    image = cv2.imread(file)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 200, 0])
    upper_green = np.array([85, 255, 255])
    lower_blue = np.array([85, 100, 100])
    upper_blue = np.array([110, 255, 255])
    lower_orange = np.array([0, 150, 150])
    upper_orange = np.array([20, 255, 255])

    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    mask = cv2.add(mask_blue, mask_green)
    mask = cv2.add(mask, mask_orange)

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((17, 17)), iterations=5)
    mask = cv2.resize(mask, dsize=(400, 400), fx=20, fy=20)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    k = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 1000:
            k += 1
            final += 1
    print(f"Карандашей на {file} - {k}")

print(f"Карандашей на всех картинках - {final}")