import cv2 as cv
from func import *

cap = cv.VideoCapture("video/Sign4.mkv")
if cap.isOpened() == False:
    print("Cannot open input video")
    exit()

vision = Vision()
b = 0
i = 0
while (cv.waitKey(1) != 27):
    ret, frame = cap.read()
    frame_copy = frame.copy()
    perspective = vision.vision_func(frame=frame_copy)
    cv.imshow("perspective", perspective)
    print(vision.angele(frame=perspective))
    stop = vision.detect_stop_line(frame=perspective)
    if stop:
        print(stop)
        b = perspective.copy()
        cv.imshow("STOP"+str(i), perspective)
        i += 1

cv.destroyAllWindows()
cap.release()
