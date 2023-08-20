import cv2
import time
import numpy as np
import handTrackingModule as htm
import volumeСhangeModule as vcm
import pyautogui
from tensorflow import keras


cap = cv2.VideoCapture(0)
p_time = 0
mode = 'None'
model = keras.models.load_model(r"D:\platinus_control_dlya_bedni\model\model_for_gestures.h5")
detector = htm.handDetector()
previous_between_tumb_and_point_x, previous_between_tumb_and_point_y = 0, 0
start_time = time.time()
time_change = 3


while True:
    sucsess, img = cap.read()

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    img = detector.findHands(img)
    landmarks_List = detector.find_position(img, hand_num=0)

    if len(landmarks_List) != 0:
        #for volume change

        wrist_x, wrist_y = landmarks_List[0][1], landmarks_List[0][2]
        tumb_x, tumb_y = landmarks_List[4][1], landmarks_List[4][2]
        point_x, point_y = landmarks_List[8][1], landmarks_List[8][2]
        middle_x, middle_y = landmarks_List[12][1], landmarks_List[12][2]

        points_for_prediction = np.array([[tumb_x, tumb_y, point_x, point_y, wrist_x, wrist_y, middle_x, middle_y]])
        prediction = model.predict(points_for_prediction)
        predicted_class = np.argmax(prediction, axis=1)

        if predicted_class == 1:
            mode = 'volume change'
            volume_change = vcm.volumeChange(tumb_x, tumb_y, point_x, point_y)
            volume_change.change_volume(img,tumb_x, tumb_y, point_x, point_y)
        elif predicted_class == 2:
            mode = 'sliding_left'
            pyautogui.hotkey('alt', 'tab')
            time.sleep(1)
        elif predicted_class == 3:
            mode = 'sliding_right'
            pyautogui.hotkey('alt', 'shift', 'tab')
            time.sleep(1)
        else:
            mode = 'None'

        cv2.putText(img, mode, (30, 90), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 3)
        

    cv2.putText(img, str(int(fps)), (30, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    