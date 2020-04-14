from func import *

class Vision:
    def __init__(self, d=0):
        self.d = d
        self.last = 0
        self.angle_pd = PD(kP=KP, kD=KD)
        self.speed = speed
    
    def vision_func (self, frame):
        image = frame.copy()
        img = cv2.resize(image, (400, 300))
        binary = binarize(img, d=self.d)
        perspective = trans_perspective(binary, TRAP, RECT, SIZE)
        return perspective

    def detect_stop_line(self, frame):
        if (frame[100][180] > 200) and (frame[100][200] > 200) and (frame[100][160] > 200):
            return True
        else:
            return False

    def angele (self, frame):
        image = frame.copy()
        left, right = centre_mass(image, d=self.d)
        angle = self.angle_pd.calc(left=left, right=right)
        if angle < 70:
            angle = 70
        elif angle > 106:
            angle = 104
        return angle
    @delay(delay=0.5)
    def stopeer_f(self):
        self.speed = stop_speed
    def run(self, frame):
        perspective = self.vision_func(frame=frame)
        self.angle = self.angele(frame=perspective)
        cv2.imshow("perspective", perspective)
        stop_line = self.detect_stop_line(frame=perspective)
        if stop_line:
            print("STOP_LINE")
            self.speed = 1450
            self.stopeer_f()
            # send_cmd('H00/' + str(speed) + '/' + str(angle) + "E")
        # else:
            # send_cmd('H00/' + '1450' + '/' + str(angle) + "E")
            # time.sleep(0.5)
            # send_cmd('H00/' + str(stop_speed) + '/' + str(angle) + "E")
        return self.angle, self.speed