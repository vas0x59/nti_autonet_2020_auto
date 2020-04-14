from  CVCapIN import CVCapIN
from Data import DataControl
from OBJDetection import OBJDetection
from LANEDetection import LANEDetection
import cv2
from FPS import FPS
from Drive import Drive
from RegSvet import RegSvet
drive_data = DataControl()
drive_data.start()
# drive_data.set("tfl", "red")
objd = OBJDetection()
objd.load()
laned = LANEDetection(drive_data)

cap = CVCapIN(id_c="./Sign_and_person.mkv")
cap.start()

drive = Drive(drive_data=drive_data)

fpser = FPS()
fpser.start()

rs = RegSvet(cap)
rs.reg_toggle(True)
rs.load_model_svm("tld.svm")
while cv2.waitKey(1) != ord("q"):
    
    # drive_data.set("tfl", "red")
    _, frame = cap.read()
    cv2.imshow("ddd", frame)
    laned_img = laned.run(frame.copy())
    cv2.imshow("laned", laned_img)
    objd_img, sss, mmm = objd.run(frame.copy())
    print(sss, mmm)
    cv2.imshow("objd", objd_img)

    drive.run()
    
    # print(str(drive_data))
    # l = rs.reg_svet(frame)
    # print(l)
    fpser.run()
    fpser.pr()
cap.stop()
