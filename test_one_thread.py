from  CVCapIN import CVCapIN
from Data import DataControl
from OBJDetection import OBJDetection
from LANEDetection import LANEDetection
import cv2
from FPS import FPS
drive_data = DataControl()
drive_data.start()
# drive_data.set("tfl", "red")
objd = OBJDetection(drive_data)
objd.load()
laned = LANEDetection(drive_data)

cap = CVCapIN(id_c=0)
cap.start()
fpser = FPS()
fpser.start()
while cv2.waitKey(1) != ord("q"):
    
    # drive_data.set("tfl", "red")
    _, frame = cap.read()
    cv2.imshow("ddd", frame)
    laned_img = laned.run(frame.copy())
    cv2.imshow("laned", laned_img)
    objd_img = objd.run(frame.copy())
    cv2.imshow("objd", objd_img)

    print(str(drive_data))
    fpser.run()
    fpser.pr()
cap.stop()
