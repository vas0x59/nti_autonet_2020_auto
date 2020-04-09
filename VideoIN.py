import numpy as np 
import cv2



class VideoIN:
    def __init__(self, res_x=640, res_y=480):
        self.res_x = res_x
        self.res_y = res_y

    def start(self):
        pass
    def stop(self):
        pass
    def read(self):
        return False, np.zeros((self.res_y, self.res_x, 3), dtype="uint8")

