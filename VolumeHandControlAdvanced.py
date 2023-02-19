import mediapipe as mp
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

######################
wCam, hCam = 640, 480
######################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
print(volRange)
minVol = volRange[0] + 40
maxVol = volRange[1]
volBar = 0
area = 0
colorVol = (255, 0, 0)
while True:

    success, img = cap.read()
    # Find hand
    img = detector.findHands(img)

    lmList, bbox = detector.findPosition(img, draw=True)
    length = 0
    volPer = 0
    volBar = 400
    vol = 0
    myMin = 25
    myMax = 200
    cx = cy = 0
    if len(lmList) != 0:
        # print(bbox)
        # When there is no hand shown then an empty list is returned
        # due to which we may get index out of bounds exception
        # print(lmList[4], lmList[8])

        # Filtering based on size
        # Based on bounding box
        # ymin - xmin and ymax - xmax
        wB, hB = bbox[2] - bbox[0], bbox[3] - bbox[1]
        area = (wB * hB) // 100
        # print(area)
        if 300 < area < 1000:
            # print('yes')
            # Find distance between index and thumb
            length, img, cx4, cy4, cx8, cy8, cx, cy = detector.findDistance(4, 8, img)
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)
            # print(length)
            # Convert Volume
            #     My range- 15-150
            #      Vol range - -64-0
            # To do this we have simple function in Numpy
            # Converts length from old range to the range to which we want to convert
            # vol = np.interp(length, [myMin, myMax], [minVol, maxVol])
            volBar = np.interp(length, [myMin, myMax], [400, 150])
            volPer = np.interp(length, [myMin, myMax], [0, 100])
            # Reduce resolution to make it smoother
            smoothness = 10
            volPer = smoothness * round(volPer / smoothness)

            # Check fingers up if down then we set the volume
            fingers = detector.fingerUp()
            print(fingers)

            # if pinky is down set volume
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)

        # drawings
        cv2.rectangle(img, (50, 150), (85, 400), colorVol, 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), colorVol, cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, colorVol, 3)

        cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
        cv2.putText(img, f'Vol set: {int(cVol)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX, 1, colorVol, 3)


    # frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    pTime = cTime

    cv2.waitKey(1)
