import math

import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.9):
       self.tipIds = [4, 8, 12, 16, 20]
       self.lmList = None
       self.results = None
       self.handLms = None
       self.mode = mode
       self.maxHands = maxHands
       self.detectionCon = detectionCon
       self.trackCon = trackCon

       self.mpHands = mp.solutions.hands
       self.hands = self.mpHands.Hands(self.mode,self.maxHands,1,self.detectionCon,self.trackCon)
       self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # The video Capture of OpenCv gives BGR
        # The Hands function takes RGB only so we need to convert to RGB
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks) Returns none if no hand else returns the x,y,z landmarks
        # If there are multiple hands then it will show info for each hand
        if self.results.multi_hand_landmarks:
            for self.handLms in self.results.multi_hand_landmarks:
                if draw:
                    # To draw the connections between all 21 points
                    self.mpDraw.draw_landmarks(img, self.handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def fingerUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 fingers
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]+20:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def findPosition(self, img, handNo=1, draw=True):
        # mpDraw.draw_landmarks(img,handLms) # We are displaying the original image so we draw landmarks on the
        # original image This draws only the 21 landmarks We can also draw the connections using this-
        xList = []
        yList = []
        xmin=xmax=ymin=ymax=0
        lmList = []
        bbox = []
        offset = 20
        if self.results.multi_hand_landmarks:

            for id, lm in enumerate(self.handLms.landmark):
                # print(id, lm)  # Each id has a corresponding landmark and each landmark has x, y, z
                # id is basically the id of one of the 21 landmarks
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        #             The color is BGR
            xmin, xmax, ymin, ymax = min(xList), max(xList), min(yList), max(yList)

            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (bbox[0]-offset, bbox[1]-offset), (bbox[2]+offset, bbox[3]+offset), (0, 255, 0), 2)
        self.lmList = lmList
        return lmList, bbox

    def findDistance(self, p1, p2, img, draw=True):
        # p1 and p2 are just point ids and not actually the coordinates
        cx4, cy4 = (self.lmList[p1][1]), (self.lmList[p1][2])
        cx8, cy8 = (self.lmList[p2][1]), (self.lmList[p2][2])
        cx = (cx4 + cx8) // 2
        cy = (cy4 + cy8) // 2

        cx4, cy4 = (self.lmList[4][1]), (self.lmList[4][2])
        cx8, cy8 = (self.lmList[8][1]), (self.lmList[8][2])
        cx = (cx4 + cx8) // 2
        cy = (cy4 + cy8) // 2
        # Do floor division only normal division gives error...

        cv2.circle(img, (cx4, cy4), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx8, cy8), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (cx4, cy4), (cx8, cy8), (255, 0, 255), 2)

        # now finding the length between the two points
        length = math.hypot(cx4-cx8, cy4-cy8)
        return length, img, cx4, cy4, cx8, cy8, cx, cy

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img, draw=True)
        lmList = detector.findPosition(img, draw=True)
        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()  # gives us the current time
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
