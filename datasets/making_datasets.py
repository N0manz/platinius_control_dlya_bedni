import cv2
import time
import handTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import pickle
import os


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
dataset = []
execution_time = 60
start_time = time.time()
save_directory = r"D:\platinus_control_dlya_bedni\datasets\volume_change_dataset\dataset_for_volume_change"


while (time.time() - start_time) < execution_time:
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

        cv2.circle(img, (tumb_x, tumb_y), 20, (255, 0, 255))
        cv2.circle(img, (point_x, point_y), 20, (255, 0, 255))
        cv2.line(img, (tumb_x, tumb_y), (point_x, point_y), (255, 0, 255), 3)
        len_of_line = math.hypot(tumb_x - point_x, tumb_y - point_y)

        cv2.circle(img, (wrist_x, wrist_y), 20, (255, 0, 255), thickness=-1)
        between_midle_and_pointer_x, between_midle_and_pointer_y = abs(point_x + middle_x) // 2, abs(point_y + middle_y) // 2
        
        cv2.circle(img, (between_midle_and_pointer_x, between_midle_and_pointer_y), 20, (255, 0, 255), thickness=-1)
        cv2.line(img, (wrist_x, wrist_y), (between_midle_and_pointer_x, between_midle_and_pointer_y), (0, 0, 255), 3)


        dx = between_midle_and_pointer_x - wrist_x
        dy = between_midle_and_pointer_y - wrist_y
        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians) * -1

        should_change_volume = len_of_line <= 40
        should_slide_right = angle_degrees >= 100 
        should_slide_left = angle_degrees <= 30

        if should_change_volume:
            mode = 1
        elif should_slide_left:
            mode = 2
        elif should_slide_right:
            mode = 3
        else:
            mode = 0

        data_point = {
            'tumb_x': tumb_x,
            'tumb_y': tumb_y,
            'point_x': point_x,
            'point_y': point_y,
            'writst_x': wrist_x,
            'wrist_y': wrist_y,
            'middle_x': middle_x,
            'middle_y': middle_y,
            'mode': mode
        }

        print(should_change_volume, should_slide_left, should_slide_right, mode)
        dataset.append(data_point)

        if (time.time() - start_time) >= execution_time:
            break
        #for sliding


        '''current_wrist_x, current_wrist_y = landmarks_List[0][1], landmarks_List[0][2]
        sliding = sm.SLIDING(current_wrist_x, current_wrist_y, previous_wrist_x, previous_wrist_y)
        sliding.slide(img, current_wrist_x, current_wrist_y, previous_wrist_x, previous_wrist_y)
        previous_wrist_x, previous_wrist_y = current_wrist_x, current_wrist_y'''


        #for wraping


    cv2.putText(img, str(int(fps)), (30, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

if not os.path.exists(save_directory):
    os.makedirs(save_directory)

dataset_filename = os.path.join(save_directory, "dataset_for_volume_change.pickle")

with open(dataset_filename, 'wb') as f:
    pickle.dump(dataset, f)

print(f"Датасет сохранен в файл {dataset_filename}")
    