import cv2
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import numpy as np

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
        cv2.circle(img, (tumb_x, tumb_y), 20, (255, 0, 255))
        cv2.circle(img, (point_x, point_y), 20, (255, 0, 255))
        cv2.line(img, (tumb_x, tumb_y), (point_x, point_y), (255, 0, 255), 3)
        len_of_line = math.hypot(tumb_x - point_x, tumb_y - point_y)
        
        if len_of_line <= 40:
            cv2.putText(img, f"current mode is volume_changing", (30, 90), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
        print(len_of_line)
        vol = np.interp(len_of_line, [20.0, 250.0], [0.0, 1.0])
        cv2.putText(img, f"current volume is {int(vol * 100)}", (30, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
        self.set_volume(vol)