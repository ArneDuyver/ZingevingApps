PICTURES = [
    ("Chinchilla", 8042, 47),
    ("Patrijs", 8043, 267),
    ("Stokstaart", 8044, 347),
    ("Wasbeer", 8046, 372),
    ("Comorenwever", 8047, 51),
    ("Cavia", 8048, 45),
    ("Stokstaart", 8050, 347),
    ("antilope", 8051, 14),
    ("kraanvogel", 8052, 188),
    ("Grijs bokje", 8055, 118),
    ("antilope", 8056, 14),
    ("gibbon", 8057, 105),
    ("Winterkoningkje", 8059, 377),
    ("Kapucijnaapje", 8060, 161),
    ("wasbeer", 8061, 372),
    ("steikel", 8062, 341),
    ("golden", 8063, 110),
    ("Klipdas", 8064, 174),
    ("labrador", 8065, 110),
    ("olifant", 8066, 245),
    ("secretarisvogel", 8069, 304),
    ("scholekster", 8071, 300),
    ("neusbeer", 8070, 238),
    ("flamingo", 8072, 83),
    ("barry", 8073, 310)
]




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



def augmentation(bbox, img, img_augment, img_augment_blurred):
    # top_left = bbox[0][0][0], bbox[0][0][1]
    # top_right = bbox[0][1][0], bbox[0][1][1]
    # bottem_right = bbox[0][2][0], bbox[0][2][1]
    # bottem_left = bbox[0][3][0], bbox[0][3][1]



    height, width, _, = img_augment.shape

    extra_margin = 15
    points_1 = np.array([
        [bbox['topleft'][0]+extra_margin, bbox['topleft'][1]-extra_margin],
        [bbox['topright'][0]-extra_margin, bbox['topright'][1]-extra_margin],
        [bbox['bottomright'][0]-extra_margin, bbox['bottomright'][1]+extra_margin],
        [bbox['bottomleft'][0]+extra_margin, bbox['bottomleft'][1]+extra_margin]
    ])
    points_2 = np.float32([[0,0],[width,0],[width,height],[0,height]])
    matrix, _ = cv2.findHomography(points_2,points_1)

    # height, width, _, = img_augment.shape
    # points_3 = np.array([
    #     [bbox['topleft'][0]+5, bbox['topleft'][1]-5],
    #     [bbox['topright'][0]-5, bbox['topright'][1]-5],
    #     [bbox['bottomright'][0]-5, bbox['bottomright'][1]+5],
    #     [bbox['bottomleft'][0]+5, bbox['bottomleft'][1]+5]
    # ])
    # points_4 = np.float32([[0,0],[width,0],[width,height],[0,height]])
    # matrix_blurred, _ = cv2.findHomography(points_4,points_3)

    image_out = cv2.warpPerspective(img_augment,matrix,(img.shape[1], img.shape[0]))
    # image_out_blurred = cv2.warpPerspective(img_augment_blurred,matrix_blurred,(img.shape[1], img.shape[0]))
    # print(np.info(image_augment), flush=True)
    # print(np.info(image_out), flush=True)

    # cv2.fillConvexPoly(img, points_3.astype(int), (0,0,0), lineType=cv2.LINE_AA)
    # image_final = img + image_out_blurred

    cv2.fillConvexPoly(img, points_1.astype(int), (0,0,0), lineType=cv2.LINE_AA)
    image_final = img + image_out

    return image_final

for totem, picid, totemid in PICTURES:

    image_augment = cv2.imread("animals/" + str(totemid) + ".jpg")
    image_augment_blurred = cv2.GaussianBlur(image_augment,(19,19),cv2.BORDER_DEFAULT)
    # cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)



    # while True:
    # _, frame = cap.read()
    # frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame = cv2.imread("input/IMG_"+str(picid)+".JPG", 1)
    frame = cv2.flip(frame, 1) # YOU ALSO NEED TO FLIP THE MARKERS
    # print(np.array(frame).shape)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = detector.detectMarkers(image=gray)
    # print(corners, flush=True)
    # if ids is not None and ids[0] == id_markerTopLeft:
    #     aruco.drawDetectedMarkers(frame, corners)
    # elif ids is not None and ids[0] == id_markerTopRight:
    #     aruco.drawDetectedMarkers(frame, corners)
    # elif ids is not None and ids[0] == id_markerBottomLeft:
    #     aruco.drawDetectedMarkers(frame, corners)
    # elif ids is not None and ids[0] == id_markerBottomRight:
    #     aruco.drawDetectedMarkers(frame, corners)
    realcorners = {
        'topleft': None,
        'topright': None,
        'bottomleft': None,
        'bottomright': None
    }


    for i in range(len(ids)):
        curid = ids[i]
        curcorner = corners[i]

        if curid is not None and curid[0] == id_markerTopLeft:
            print("id_markerTopLeft", curcorner, flush=True)
            realcorners['topleft'] = curcorner[0][1][0], curcorner[0][1][1]
        elif curid is not None and curid[0] == id_markerTopRight:
            print("id_markerTopRight", curcorner, flush=True)
            realcorners['topright'] = curcorner[0][0][0], curcorner[0][0][1]
        elif curid is not None and curid[0] == id_markerBottomLeft:
            print("id_markerBottomLeft", curcorner, flush=True)
            realcorners['bottomleft'] = curcorner[0][2][0], curcorner[0][2][1]
        elif curid is not None and curid[0] == id_markerBottomRight:
            print("id_markerBottomRight", curcorner, flush=True)
            realcorners['bottomright'] = curcorner[0][3][0], curcorner[0][3][1]

    print(realcorners, flush=True)

    # cv2.imshow('input', frame)

    pressedKey = cv2.waitKey(1) & 0xFF

    # if pressedKey == 27:
    #     break
    # elif pressedKey == ord('a'):
    #     print('a is pressed')
        # image_screenshot = pyautogui.screenshot()
        # image_screenshot = cv2.cvtColor(np.array(image_screenshot), cv2.COLOR_RGB2BGR)
    # cropped_screenshot = pyautogui.screenshot(region=(700,108,1000,467))
    # cropped_screenshot = cv2.cvtColor(np.array(cropped_screenshot), cv2.COLOR_RGB2BGR)
    # newframe = augmentation(corners)
    newframe = augmentation(realcorners, frame, image_augment, image_augment_blurred)
    newframe = np.flip(newframe, 1)
    cv2.imwrite("output/" + str(picid) + "-" + totem + ".jpg", newframe)
    print("output/" + str(picid) + "-" + totem + ".jpg", flush=True)

# cv2.destroyAllWindows
import os
os.system("pause")
