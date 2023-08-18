import cv2
import mediapipe as mp
import time
class handDetector():
    def __init__(self, mode=False, max_hands=2):
        self.mode = mode
        self.max_hands = max_hands

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands, min_detection_confidence=0.5)

        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def find_position(self, img, hand_num):
        lmList = []
        if self.results.multi_hand_landmarks:
            current_hand = self.results.multi_hand_landmarks[hand_num]

            for id, lm in enumerate(current_hand.landmark):
                    heigth, width, chanels = img.shape
                    center_x, center_y = int(lm.x * width), int(lm.y * heigth)
                    lmList.append([id, center_x, center_y])
        return lmList

def main():
    cap = cv2.VideoCapture(0)
    p_time = 0
    c_time = 0
    detector = handDetector()
    while True:
        success, img = cap.read()
        
        img = detector.findHands(img)
        lmList = detector.find_position(img, hand_num=0)
        if len(lmList) != 0:
            print(lmList[4])
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow('Image', img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()