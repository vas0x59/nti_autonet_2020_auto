import cv2 as cv
from func import *
from TaskClasses import *
cap = cv.VideoCapture("Videos/Sign3.mkv")
if cap.isOpened() == False:
    print("Cannot open input video")
    exit()

# vision = VisionStopSign()
# vision = Vision()
vision = VisionSignHist()
b = 0
i = 0
while (cv.waitKey(1) != 27):
    ret, frame = cap.read()
    # frame_copy = frame.copy()
    # perspective = vision.vision_func(frame=frame_copy)
    # cv.imshow("perspective", perspective)
    # print(vision.angele(frame=perspective))
    # stop = vision.detect_stop_line(frame=perspective)
    # if stop:
    #     print(stop)
    #     b = perspective.copy()
    #     cv.imshow("STOP"+str(i), perspective)
    #     i += 1
    ang, spd = vision.run(frame.copy())
    print(ang, spd)
    if vision.exit == True:
        break

cv.destroyAllWindows()
cap.release()