import cv2
import mediapipe as mp
import time
import numpy as np
import handTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

def set_volume(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_object = cast(interface, POINTER(IAudioEndpointVolume))
    volume_object.SetMasterVolumeLevelScalar(volume, None)

cap = cv2.VideoCapture(0)
p_time = 0

detector = htm.handDetector()

while True:
    sucsess, img = cap.read()

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    img = detector.findHands(img)
    lmList = detector.find_position(img, hand_num=0)

    if len(lmList) != 0:
        tumb_x, tumb_y = lmList[4][1], lmList[4][2]
        point_x, point_y = lmList[8][1], lmList[8][2]

        cv2.circle(img, (tumb_x, tumb_y), 20, (255, 0, 255))
        cv2.circle(img, (point_x, point_y), 20, (255, 0, 255))
        cv2.line(img, (tumb_x, tumb_y), (point_x, point_y), (255, 0, 255), 3)
        len_of_line = math.hypot(tumb_x - point_x, tumb_y - point_y)

        vol = np.interp(len_of_line, [20.0, 250.0], [0.0, 1.0])
        set_volume(vol)

    cv2.putText(img, str(int(fps)), (40, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    