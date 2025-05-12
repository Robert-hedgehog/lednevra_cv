import cv2
import numpy as np

video = cv2.VideoCapture('output.avi')
final = 0
while True:
    check, image = video.read()
    if not check:
        break

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([50, 100, 70])
    upper_green = np.array([70, 255, 255])

    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area == 2024.5:
            final += 1

video.release()

print(f"Моих картинок - {final}")



