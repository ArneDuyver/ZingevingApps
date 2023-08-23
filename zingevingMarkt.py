import cv2
import cv2.aruco as aruco
import numpy as np
import pyautogui

id_markerTopLeft = 7
id_markerTopRight = 8
id_markerBottomLeft = 9
id_markerBottomRight = 10

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

image_augment = cv2.imread("lowpolyantilope2.png")

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

def augmentation(bbox, img, img_augment):
    top_left = bbox[0][0][0], bbox[0][0][1]
    top_right = bbox[0][1][0], bbox[0][1][1]
    bottem_right = bbox[0][2][0], bbox[0][2][1]
    bottem_left = bbox[0][3][0], bbox[0][3][1]

    height, width, _, = img_augment.shape
    points_1 = np.array([top_left,top_right,bottem_right,bottem_left])
    points_2 = np.float32([[0,0],[width,0],[width,height],[0,height]])

    matrix, _ = cv2.findHomography(points_2,points_1)
    image_out = cv2.warpPerspective(img_augment,matrix,(img.shape[1], img.shape[0]))
    cv2.fillConvexPoly(img, points_1.astype(int), (0,0,0))
    image_out = img + image_out

    return image_out


while True:
    _, frame = cap.read()
    # frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame = cv2.flip(frame, 1) # YOU ALSO NEED TO FLIP THE MARKERS

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    corners, ids, rejected = detector.detectMarkers(image=gray)
    # print(corners)
    if ids is not None and ids[0] == id_markerTopLeft:
        aruco.drawDetectedMarkers(frame, corners)
        frame = augmentation(np.array(corners)[0], frame, image_augment)
    elif ids is not None and ids[0] == id_markerTopRight:
        aruco.drawDetectedMarkers(frame, corners)
    elif ids is not None and ids[0] == id_markerBottomLeft:
        aruco.drawDetectedMarkers(frame, corners)
    elif ids is not None and ids[0] == id_markerBottomRight:
        aruco.drawDetectedMarkers(frame, corners)

    cv2.imshow('input', frame)
    
    pressedKey = cv2.waitKey(1) & 0xFF
    if pressedKey == 27:
        break
    elif pressedKey == ord('a'):
        print('a is pressed')
        # image_screenshot = pyautogui.screenshot()
        # image_screenshot = cv2.cvtColor(np.array(image_screenshot), cv2.COLOR_RGB2BGR)
        cropped_screenshot = pyautogui.screenshot(region=(700,108,1000,467))
        cropped_screenshot = cv2.cvtColor(np.array(cropped_screenshot), cv2.COLOR_RGB2BGR)
        cv2.imwrite("screenshot.png", cropped_screenshot)

cv2.destroyAllWindows