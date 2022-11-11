import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('capture.png', 1)
img2 = img.copy()
map_selector = cv.imread('map-selector.png', 1)
cup_selector = cv.imread('cup-selector.png', 1)
_, w, h = map_selector.shape[::-1]
# All the 6 methods for comparison in a list

cv.startWindowThread()
cap = cv.VideoCapture("/dev/apfs-raw-device.2.0")

if not cap.isOpened():
    print("Cannot open camera")
    exit()

threshold = 600
method = cv.TM_CCORR_NORMED

cup = False
map = False

while(True):
    # reading the frame
    ret, frame = cap.read()
    # displaying the frame

    res1 = cv.matchTemplate(frame, cup_selector, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res1)

    cv.rectangle(frame, (0, threshold), (1000, threshold), 125, 2)

    if max_loc[1] < threshold and cup is False:
        print("got cup at: ", max_loc)
        bottom_right = (max_loc[0] + w, max_loc[1] + h)
        cv.rectangle(frame, max_loc, bottom_right, 125, 2)

    if cv.waitKey(1) & 0xFF == ord('q'):
        cup = True

    # Get Map

    res2 = cv.matchTemplate(frame, map_selector, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res2)
    if max_loc[1] > threshold and cup is True:
        print("got map at:", max_loc)
        bottom_right = (max_loc[0] + w, max_loc[1] + h)
        cv.rectangle(frame, max_loc, bottom_right, 255, 2)

    cv.imshow('frame', frame)


cap.release()
cv.destroyAllWindows()
# the following is necessary on the mac,
# maybe not on other platforms:
cv.waitKey(1)


while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv.imshow('frame', frame)
    continue
    # Get cup
