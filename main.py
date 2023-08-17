import cv2
import mediapipe as mp
import time
import numpy as np
import handTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import volumeСhangeModule as vcm
import pyautogui
import slidingModule as sm

def set_volume(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_object = cast(interface, POINTER(IAudioEndpointVolume))
    volume_object.SetMasterVolumeLevelScalar(volume, None)

cap = cv2.VideoCapture(0)
p_time = 0
previous_wrist_x = 0
previous_wrist_y = 0


detector = htm.handDetector()

while True:
    sucsess, img = cap.read()

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    img = detector.findHands(img)
    landmarks_List = detector.find_position(img, hand_num=0)

    if len(landmarks_List) != 0:
        #for volume change


        tumb_x, tumb_y = landmarks_List      [4][1], landmarks_List[4][2]
        point_x, point_y = landmarks_List[8][1], landmarks_List[8][2]
        volume_change = vcm.volumeChange(tumb_x, tumb_y, point_x, point_y)
        volume_change.change_volume(img,tumb_x, tumb_y, point_x, point_y)


        #for sliding


        current_wrist_x, current_wrist_y = landmarks_List[0][1], landmarks_List[0][2]
        sliding = sm.SLIDING(current_wrist_x, current_wrist_y, previous_wrist_x, previous_wrist_y)
        sliding.slide(img, current_wrist_x, current_wrist_y, previous_wrist_x, previous_wrist_y)
        previous_wrist_x, previous_wrist_y = current_wrist_x, current_wrist_y


        #for wraping


    cv2.putText(img, str(int(fps)), (30, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    