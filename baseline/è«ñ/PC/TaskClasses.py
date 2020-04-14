from func import *
from OBJDetection import OBJDetection
class Vision:
    def __init__(self, d=0):
        self.d = d
        self.last = 0
        self.angle_pd = PD(kP=KP, kD=KD)
        self.speed = speed
        self.exit = False
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
        # exit()
        time.sleep(0.1)
        self.exit = True
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

class VisionStopSign:
    def __init__(self, d=0):
        self.d = d
        self.last = 0
        self.angle_pd = PD(kP=KP, kD=KD)
        self.speed = speed
        self.objd = OBJDetection()
        self.signs = []
        self.sign = "none"
        self.sign_hist = []
        self.objd.load()
        self.exit = False
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
        time.sleep(0.1)
        self.exit = True
        # exit()
    def run(self, frame):
        img_out, ssnow, self.sign = self.objd.run(frame.copy())
        perspective = self.vision_func(frame=frame)
        self.angle = self.angele(frame=perspective)
        cv2.imshow("perspective", perspective)
        cv2.imshow("img_out", img_out)
        # stop_line = self.detect_stop_line(frame=perspective)
        # if stop_line:
        #     print("STOP_LINE")
        #     self.speed = 1450
        #     self.stopeer_f()
            # send_cmd('H00/' + str(speed) + '/' + str(angle) + "E")
        # else:
            # send_cmd('H00/' + '1450' + '/' + str(angle) + "E")
            # time.sleep(0.5)
            # send_cmd('H00/' + str(stop_speed) + '/' + str(angle) + "E")
        # if slen(elf.sign_hist
        if self.sign == "stop":
            self.speed = 1450
            self.stopeer_f()
            # exit()
        # if self.sign != "none" and self.sign_hist[-1]:
        #     self.sign_hist += [self.sign]
        return self.angle, self.speed


class VisionSignHist:
    def __init__(self, d=0):
        self.d = d
        self.last = 0
        self.angle_pd = PD(kP=KP, kD=KD)
        self.speed = speed
        self.objd = OBJDetection()
        self.signs = []
        self.sign = "none"
        self.sign_hist = []
        self.objd.load()
        self.exit = False
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
        time.sleep(0.1)
        self.exit = True
        # exit()
    def run(self, frame):
        img_out, ssnow, self.sign = self.objd.run(frame.copy(), thresh=16)
        perspective = self.vision_func(frame=frame)
        self.angle = self.angele(frame=perspective)
        cv2.imshow("perspective", perspective)
        cv2.imshow("img_out", img_out)
        # stop_line = self.detect_stop_line(frame=perspective)
        # if stop_line:
        #     print("STOP_LINE")
        #     self.speed = 1450
        #     self.stopeer_f()
            # send_cmd('H00/' + str(speed) + '/' + str(angle) + "E")
        # else:
            # send_cmd('H00/' + '1450' + '/' + str(angle) + "E")
            # time.sleep(0.5)
            # send_cmd('H00/' + str(stop_speed) + '/' + str(angle) + "E")
        # if slen(elf.sign_hist
        # if self.sign == "stop":
        #     self.speed = 1450
        #     self.stopeer_f()
            # exit()
        if len(self.sign_hist) == 0 and self.sign != "none":
            self.sign_hist += [self.sign]
        elif self.sign != "none" and self.sign_hist[-1] != self.sign:
            self.sign_hist += [self.sign]
        print(self.sign_hist)
        return self.angle, self.speed