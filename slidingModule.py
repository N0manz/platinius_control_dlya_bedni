
import pyautogui
import cv2
import math
import handTrackingModule as htm
import time

class SLIDING():
    def __init__(self, wrist_x, wrist_y, middle_x, middle_y, pointer_x, pointer_y):

        self.wrist_x = wrist_x
        self.wrist_y = wrist_y
        self.middle_x = middle_x
        self.midle_y = middle_y
        self.pointer_x = pointer_x
        self.pointer_y = pointer_y

    def slide(self,img, wrist_x, wrist_y, middle_x, middle_y, pointer_x, pointer_y):

        cv2.circle(img, (wrist_x, wrist_y), 20, (255, 0, 255), thickness=-1)
        between_midle_and_pointer_x, between_midle_and_pointer_y = abs(pointer_x + middle_x) // 2, abs(pointer_y + middle_y) // 2
        
        cv2.circle(img, (between_midle_and_pointer_x, between_midle_and_pointer_y), 20, (255, 0, 255), thickness=-1)
        cv2.line(img, (wrist_x, wrist_y), (between_midle_and_pointer_x, between_midle_and_pointer_y), (0, 0, 255), 3)


        dx = between_midle_and_pointer_x - wrist_x
        dy = between_midle_and_pointer_y - wrist_y
        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians) * -1

        cv2.putText(img, str(int(angle_degrees)), (10, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        '''len_of_line = math.hypot(current_wrist_x - previous_wrist_x, current_wrist_y - previous_wrist_y)
        if previous_wrist_x > current_wrist_x:
            len_of_line *= -1

        if len_of_line >= 75:
            pyautogui.hotkey('alt', 'tab')
        elif len_of_line <= -75:
            pyautogui.hotkey('alt', 'shift', 'tab')
        print(len_of_line)'''

def main():
    cap = cv2.VideoCapture(0)
    p_time = 0
    c_time = 0
    detector = htm.handDetector()
    while True:
        _, img = cap.read()
        
        img = detector.findHands(img)
        landmark_list = detector.find_position(img, hand_num=0)
        if len(landmark_list) != 0:
            wrist_x, wrist_y = landmark_list[0][1], landmark_list[0][2]
            middle_x, middle_y = landmark_list[12][1], landmark_list[12][2]
            pointer_x, pointer_y = landmark_list[8][1], landmark_list[8][2]

            sliding = SLIDING(wrist_x, wrist_y, middle_x, middle_y, pointer_x, pointer_y)
            sliding.slide(img, wrist_x, wrist_y, middle_x, middle_y, pointer_x, pointer_y)
            
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow('Image', img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()