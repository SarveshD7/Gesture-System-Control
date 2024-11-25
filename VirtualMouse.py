import cv2
import numpy as np
import HandTrackingModule as htm
import autopy
import time

################
wCam = 640
hCam = 480
cTime = pTime = 0
wScr, hScr = autopy.screen.size()
frameR = 100
smoothening = 7
pX, pY = 0, 0
cX, cY = 0, 0
#################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
# print(wScr, hScr)
while True:
    success, img = cap.read()
    # 1. Find hand Landmarks
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of middle and index finger
    if len(lmList) != 0:
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

        # 3. Check which fingers are up
        fingers = detector.fingerUp()
        # print(fingers)

        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert coordinates
            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            # 6. Smoothen values
            cX = pX + (x3 - pX) / smoothening
            cY = pY + (y3 - pY) / smoothening

            # 7. Move Mouse
            # The pointer is moving opposite to our finger movement. So flip
            autopy.mouse.move(wScr-cX, cY)
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), -1)
            pX, pY = cX, cY
        # 8. Clicking mode - When both index and middle finger are up
        if fingers[1] == 1 and fingers[2] == 1:
            #     The clicking style gesture logic
            length, img,a,b,c,d,e,f = detector.findDistance(8, 12, img)
            if length <= 40:
                autopy.mouse.click()
    # 11. Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
