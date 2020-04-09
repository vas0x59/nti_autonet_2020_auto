from  VideoIN import VideoIN
import cv2
class CVCapIN(VideoIN):
    def __init__(self, res_x=640, res_y=480, id_c=0):
        self.res_x = res_x
        self.res_y = res_y
        self.id = id_c

    def start(self):
        # return 0
        self.cap = cv2.VideoCapture(self.id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.res_x))
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.res_y))
    def stop(self):
        self.cap.release()
    def read(self):
        return self.cap.read()
