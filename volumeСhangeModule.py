import cv2
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import numpy as np
import handTrackingModule as htm
import time

class volumeChange():
    def __init__(self, tumb_x, tumb_y, point_x, point_y):
        self.tumb_x = tumb_x
        self.tumb_y = tumb_y
        self.point_x = point_x
        self.point_y = point_y
        
    def set_volume(self, volume):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_object = cast(interface, POINTER(IAudioEndpointVolume))
        volume_object.SetMasterVolumeLevelScalar(volume, None)

    def change_volume(self, img, tumb_x, tumb_y, point_x, point_y):
        len_of_line = 0
        cv2.circle(img, (tumb_x, tumb_y), 20, (255, 0, 255))
        cv2.line(img, (tumb_x, tumb_y), (point_x, point_y), (255, 0, 255), 3)

        len_of_line = math.hypot(point_x - tumb_x, point_y, tumb_y)
        print(len_of_line)
        vol = np.interp(len_of_line, [240.0, 500.0], [0.0, 1.0])
        cv2.putText(img, f"current volume is {int(vol * 100)}", (30, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
        self.set_volume(vol)

def main():
    cap = cv2.VideoCapture(0)
    p_time = 0
    c_time = 0
    detector = htm.handDetector()
    
    while True:
        success, img = cap.read()
        
        img = detector.findHands(img)
        landmarks_List = detector.find_position(img, hand_num=0)
        if len(landmarks_List) != 0:
            tumb_x, tumb_y = landmarks_List[4][1], landmarks_List[4][2]
            point_x, point_y = landmarks_List[8][1], landmarks_List[8][2]
            volume_change = volumeChange(tumb_x, tumb_y, point_x, point_y)
            volume_change.change_volume(img,tumb_x, tumb_y, point_x, point_y)
            
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow('Image', img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()