from  CVCapIN import CVCapIN
from Data import DataControl
# from OBJDetection import OBJDetection
from LANEDetection import LANEDetection
import cv2

drive_data = DataControl()
drive_data.start()
# drive_data.set("tfl", "red")
# objd = OBJDetection(drive_data)
laned = LANEDetection(drive_data)

cap = CVCapIN(id_c=0)
cap.start()

while cv2.waitKey(1) != ord("q"):
    
    # drive_data.set("tfl", "red")
    _, frame = cap.read()
    cv2.imshow("ddd", frame)
    laned_img = laned.run(frame)
    cv2.imshow("laned", laned_img)
    # laned.write_data()
    # objd.run(frame)
    # objd.write_data()

    print(str(drive_data))

cap.stop()
