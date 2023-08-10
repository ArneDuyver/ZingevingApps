import cv2
import numpy as np

video = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
bg = cv2.imread("hawaii_bg.png")

while True:
    res, frame = video.read()
    # frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame = cv2.flip(frame, 1)

    frame = cv2.resize(frame, (640,480))
    bg = cv2.resize(bg, (640,480))

    hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    u_green = np.array([194, 194, 196])
    l_green = np.array([109, 110, 114])
    mask = cv2.inRange(frame,l_green,u_green)
    res = cv2.bitwise_and(frame,frame, mask=mask)

    f = frame - res
    f = np.where(f==0, bg, f)

    # cv2.imshow('video', frame)
    cv2.imshow('mask', f)

    pressedKey = cv2.waitKey(1) & 0xFF
    if pressedKey == 27:
        break