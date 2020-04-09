from  CVCapIN import CVCapIN
import cv2

cap = CVCapIN(id_c=0)
cap.start()

while cv2.waitKey(1) != ord("q"):
    _, frame = cap.read()
    cv2.imshow("ddd", frame)

cap.stop()
