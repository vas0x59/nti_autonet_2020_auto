import cv2

import CVCapIN
from OpticalFlow import OpticalFlow

from FPS import FPS


# drive_data = DataControl()
# drive_data.start()
# drive_data.set("tfl", "red")
# objd = OBJDetection(drive_data)
# objd.load()
# laned = LANEDetection(drive_data)

cap = CVCapIN.CVCapIN(id_c=2)
cap.start()

# drive = Drive()
optf = OpticalFlow()
fpser = FPS()
fpser.start()
while cv2.waitKey(1) != ord("q"):
    
    # drive_data.set("tfl", "red")
    _, frame = cap.read()
    # cv2.imshow("ddd", frame)
    # laned_img = laned.run(frame.copy())
    # cv2.imshow("laned", laned_img)
    # objd_img = objd.run(frame.copy())
    # cv2.imshow("objd", objd_img)

    # drive.run()
    
    # print(str(drive_data))
    optf_img = optf.run(frame)
    cv2.imshow("optf_img", optf_img)
    fpser.run()
    # fpser.pr()
cap.stop()

