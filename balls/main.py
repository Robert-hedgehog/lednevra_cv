import cv2
import numpy as np
import subprocess
import os
import json
import random

# Переключить в ручной режим экспозиции
subprocess.run(["v4l2-ctl", "-d", "/dev/video0", "-c", "auto_exposure=1"])
# Установить значение экспозиции
subprocess.run(["v4l2-ctl", "-d", "/dev/video0", "-c", "exposure_time_absolute=200"])

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

def get_color(image):
    x, y, w, h = cv2.selectROI("Color selection", image)
    x, y, w, h = int(x), int(y), int(w), int(h)
    roi = image[y:y+h, x:x+w]
    color = (np.median(roi[:, :, 0]),
            np.median(roi[:, :, 1]),
            np.median(roi[:, :, 2]))
    cv2.destroyWindow("Color selection")
    return color

def get_ball(image, color):
    lower = (np.max([0, color[0] - 5]), color[1] * 0.8, color[2] * 0.8)
    upper = (color[0] + 5, 255, 255)
    mask = cv2.inRange(image, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        contour = max(contours, key = cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(contour)
        return True, (int(x), int(y), int(radius), mask)
    return False, (-1, -1, -1, np.array([]))

file_name = "settings.json"
if os.path.exists(file_name):
    base_colors = json.load(open(file_name, "r"))
else:
    base_colors = {}

game_started = False
guess_colors = []

while capture.isOpened():
    ret, frame = capture.read()
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    key = chr(cv2.waitKey(1) & 0xFF)
    if key in "123":
        color = get_color(hsv)
        base_colors[key] = color
    if key == "q":
        break
    consistency_x = {}
    consistency_y = {}
    for key in base_colors:
        retr, (x, y, radius, mask) = get_ball(hsv, base_colors[key])
        consistency_x[key] = x
        consistency_y[key] = y
        if retr:
            cv2.circle(frame, (x, y), radius, (255, 0, 255), 2)

    if len(base_colors) == 3:
        if not game_started:
            guess_colors = list(base_colors)
            random.shuffle(guess_colors)
            game_started = True
            print(guess_colors)
        else:
            if all(x >= 0 for x in consistency_x.values()) or all(y >= 0 for y in consistency_x.values()):
                xx = sorted(consistency_x, key = consistency_x.get)
                yy = sorted(consistency_y, key = consistency_y.get)
                if xx == guess_colors or yy == guess_colors:
                    capture.release()
                    cv2.putText(frame, f"You win", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,(255, 255, 0))
                    cv2.imshow("Camera", frame)
                    cv2.waitKey()

    cv2.putText(frame, f"Game started = {game_started}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0))
    cv2.imshow("Camera", frame)

capture.release()
cv2.destroyAllWindows()

json.dump(base_colors, open(file_name, "w"))