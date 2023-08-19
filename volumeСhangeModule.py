import cv2
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import numpy as np

class volumeChange():
    def __init__(self, tumb_x, tumb_y, point_x, point_y, previous_between_tumb_and_point_x, previous_between_tumb_and_point_y):
        self.tumb_x = tumb_x
        self.tumb_y = tumb_y
        self.point_x = point_x
        self.point_y = point_y
        self.previous_between_tumb_and_point_x = previous_between_tumb_and_point_x
        self.previous_between_tumb_and_point_y = previous_between_tumb_and_point_y
        
    def set_volume(self, volume):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_object = cast(interface, POINTER(IAudioEndpointVolume))
        volume_object.SetMasterVolumeLevelScalar(volume, None)

    def change_volume(self, img, tumb_x, tumb_y, point_x, point_y, previous_between_tumb_and_point_x, previous_between_tumb_and_point_y):
        cv2.circle(img, (tumb_x, tumb_y), 20, (255, 0, 255))
        cv2.line(img, (tumb_x, tumb_y), (point_x, point_y), (255, 0, 255), 3)
        between_tumb_and_point_x, between_tumb_and_point_y = (tumb_x + point_x) // 2, (tumb_y + point_y) // 2

        len_of_line = math.hypot(between_tumb_and_point_x - previous_between_tumb_and_point_x, between_tumb_and_point_y - previous_between_tumb_and_point_y)
        
        print(len_of_line)
        vol = np.interp(len_of_line, [tumb_y, point_y], [0.0, 1.0])
        cv2.putText(img, f"current volume is {int(vol * 100)}", (30, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
        self.set_volume(vol)