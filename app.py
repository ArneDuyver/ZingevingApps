from flask import Flask,render_template,Response
import cv2
import cv2.aruco as aruco
import numpy as np
import pyautogui

app=Flask(__name__)
camera=cv2.VideoCapture(0)

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

imagestr = "lowpolyantilope2.png"
savestr = "screenshot.png"
imagestr2 = "Picture1.png"

image_augment = cv2.imread(imagestr, cv2.IMREAD_UNCHANGED)
image_augment2 = cv2.imread(imagestr2, cv2.IMREAD_UNCHANGED)

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
    # TODO just do this as a background and then layer the rest on top
    cv2.fillConvexPoly(img, points_1.astype(int), (255,255,255))
    # image_out = img + image_out

    imga = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    image_outa = cv2.cvtColor(image_out, cv2.COLOR_RGB2RGBA)
    image_outOut = imga + image_outa

    return image_outOut


def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
        # frame[:, :, 3] = 255
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = detector.detectMarkers(image=gray)
        arr =  np.empty(shape = [1,4,2])
        if ids is not None and len(ids) == 4:
            for i in range(0,3):
                if ids is not None and ids[i] == 7:
                    arr[0][1] = np.array(corners)[i][0][1]
                if ids is not None and ids[i] == 8:
                    arr[0][0] = np.array(corners)[i][0][0]
                if ids is not None and ids[i] == 9:
                    arr[0][2] = np.array(corners)[i][0][2]
                if ids is not None and ids[i] == 10:
                    arr[0][3] = np.array(corners)[i][0][3]
            frame = augmentation(arr, frame, image_augment)
            frame = augmentation(arr, frame, image_augment2)
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.png',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/screenshot', methods=['GET'])
def backend():
    cropped_screenshot = pyautogui.screenshot(region=(10,230,580,500))
    cropped_screenshot = cv2.cvtColor(np.array(cropped_screenshot), cv2.COLOR_RGB2BGR)
    cv2.imwrite(savestr, cropped_screenshot)
    return "SMILLLEEEEE!"

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=False)