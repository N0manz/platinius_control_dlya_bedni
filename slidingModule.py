
import pyautogui
import cv2
import math

class SLIDING():
    def __init__(self, current_wrist_x, current_wrist_y, previous_wrist_x=0, previous_wrist_y=0):

        self.current_wrist_x = current_wrist_x
        self.current_wrist_y = current_wrist_y
        self.previous_wrist_x = previous_wrist_x
        self.previous_wrist_y = previous_wrist_y

    def slide(self,img, current_wrist_x, current_wrist_y, previous_wrist_x, previous_wrist_y):

        cv2.circle(img, (current_wrist_x, current_wrist_y), 20, (255, 0, 255))
        cv2.line(img, (current_wrist_x, current_wrist_y), (previous_wrist_x, previous_wrist_y), (0, 0, 255), 3)

        len_of_line = math.hypot(current_wrist_x - previous_wrist_x, current_wrist_y - previous_wrist_y)
        if previous_wrist_x > current_wrist_x:
            len_of_line *= -1

        if len_of_line >= 75:
            pyautogui.hotkey('alt', 'tab')
        elif len_of_line <= -75:
            pyautogui.hotkey('alt', 'shift', 'tab')
        print(len_of_line)