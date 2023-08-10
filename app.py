from flask import Flask,render_template,Response
import cv2
import cv2.aruco as aruco
import numpy as np
import pyautogui

app=Flask(__name__)
camera=cv2.VideoCapture(0)
id_marker = 7

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

image_augment = cv2.imread("lowpolyantilope2.png")

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


def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = detector.detectMarkers(image=gray)
        if ids is not None and ids[0] == id_marker:
            frame = augmentation(np.array(corners)[0], frame, image_augment)
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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
    cv2.imwrite("screenshot.png", cropped_screenshot)
    return "SMILLLEEEEE!"

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=False)