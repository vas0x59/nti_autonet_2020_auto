from func import *
from OBJDetection import OBJDetection


class Vision:
    def __init__(self, d=0):
        self.d = d
        self.last = 0
        self.angle_pd = PD(kP=KP, kD=KD)
        self.speed = speed
        self.exit = False

    def vision_func(self, frame):
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

    def angele(self, frame):
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

    def vision_func(self, frame):
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

    def angele(self, frame):
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
        img_out, ssnow, self.sign, svet_sign, person = self.objd.run(frame.copy())
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
            self.speed = 1525
            self.stopeer_f()
            # exit()
        # if self.sign != "none" and self.sign_hist[-1]:
        #     self.sign_hist += [self.sign]
        return self.angle, self.speed


class VisionPersonStop:
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
        # self.svet_enbale  = False
        self.objd.svet_enable = False
        self.objd.sign_enable = False

    def vision_func(self, frame):
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

    def angele(self, frame):
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
        img_out, ssnow, self.sign, svet_sign, person = self.objd.run(frame.copy(), conf=0.2)
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
        if person == True:
            self.speed = 1500
            self.stopeer_f()
            # exit()
        # if self.sign != "none" and self.sign_hist[-1]:
        #     self.sign_hist += [self.sign]
        return self.angle, self.speed

class VisionPersonCounter:
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
        # self.svet_enbale  = False
        self.objd.svet_enable = False
        self.objd.sign_enable = False

    def vision_func(self, frame):
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

    def angele(self, frame):
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
        img_out, ssnow, self.sign, svet_sign, person = self.objd.run(frame.copy(), conf=0.05)
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
        print("COUNT", self.objd.person_calc)
        # if person == True:
        #     self.speed = 1500
        #     self.stopeer_f()
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

    def vision_func(self, frame):
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

    def angele(self, frame):
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
        img_out, ssnow, self.sign, svet_sign, person = self.objd.run(frame.copy(), thresh=15, conf=0.3)

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


class VisionSvetGO:
    def __init__(self, d=0):
        self.d = d
        self.last = 0
        self.angle_pd = PD(kP=KP, kD=KD)
        self.speed = speed
        self.exit = False
        self.need_svet = False
        self.objd = OBJDetection()
        self.signs = []
        self.sign = "none"
        self.sign_hist = []
        self.objd.load()
        self.pov = 0
        self.go = 0
        self.next = 0
        self.objd.svet_enable = True
        self.objd.sign_enable = False
        # self.need_svet = False

    def vision_func(self, frame):
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

    def angele(self, frame):
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
        # self.exit = True
        self.need_svet = True

    def run(self, frame):
        svet_sign = "none"
        if self.need_svet == True:
            img_out, ssnow, self.sign, svet_sign, person = self.objd.run(frame.copy(), thresh=15, conf=0.5)
            cv2.imshow("img_out", img_out)
        perspective = self.vision_func(frame=frame)
        cv2.imshow("perspective", perspective)
        if self.pov == 0:
            self.angle = self.angele(frame=perspective)
            stop_line = self.detect_stop_line(frame=perspective)
            if stop_line:
                print("STOP_LINE")
                self.speed = 1500
                self.stopeer_f()
                self.pov = 1
        else:
            if self.go == 0:
                if self.need_svet:
                    if svet_sign == "green":
                        self.need_svet = False
                        self.go = 1
                        self.angle = 87
                        self.speed = speed
                    else:
                        self.go = 0
                        self.speed = stop_speed
            else:
                left, right = centre_mass(perspective.copy())
                if left >= 150 and self.next == 0:
                    self.next += 1
                elif left < 150 and self.next == 1:
                    self.next += 1
                if self.next <= 1:
                    self.angle = 87
                else:
                    self.next = 0
                    self.pov = 0
                    self.go = 0

        return self.angle, self.speed


class VisionSvetGONoStop:
    def __init__(self, d=0):
        self.d = d
        self.last = 0
        self.angle_pd = PD(kP=KP, kD=KD)
        self.speed = 1500
        self.exit = False
        self.need_svet = True
        self.objd = OBJDetection()
        self.signs = []
        self.sign = "none"
        self.sign_hist = []
        self.objd.load()
        self.pov = 1
        self.go = 0
        self.next = 0
        self.objd.svet_enable = True
        self.objd.sign_enable = False
        # self.need_svet = False

    def vision_func(self, frame):
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

    def angele(self, frame):
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
        # self.exit = True
        self.need_svet = True

    def run(self, frame):
        svet_sign = "none"
        perspective = self.vision_func(frame=frame)
        if self.need_svet == True:
            img_out, ssnow, self.sign, svet_sign, person = self.objd.run(frame.copy(), thresh=15, conf=0.5)
            cv2.imshow("img_out", img_out)
        else:
            self.angle = self.angele(frame=perspective)
        cv2.imshow("perspective", perspective)
        if self.go == 0:
            if self.need_svet:
                if svet_sign == "green":
                    self.need_svet = False
                    self.go = 1
                    self.angle = 87
                    self.speed = speed
                else:
                    self.go = 0
                    self.speed = stop_speed
        else:
            left, right = centre_mass(perspective.copy())
            if left >= 150 and self.next == 0:
                self.next += 1
            elif left < 150 and self.next == 1:
                self.next += 1
            if self.next <= 1:
                self.angle = 87
            else:
                self.next = 0
                self.pov = 0
                self.go = 0

        return self.angle, self.speed


class VisionSvetReg:
    def __init__(self, d=0):
        self.d = d
        self.last = 0
        self.angle_pd = PD(kP=KP, kD=KD)
        self.speed = 1500
        self.exit = False
        self.need_svet = False
        self.objd = OBJDetection()
        self.signs = []
        self.sign = "none"
        self.sign_hist = []
        self.objd.load()
        self.objd.svet_enable = True
        self.objd.sign_enable = False

    def vision_func(self, frame):
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

    def angele(self, frame):
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
        # self.exit = True
        self.need_svet = True

    def run(self, frame):
        img_out, ssnow, self.sign, svet_sign, person = self.objd.run(frame.copy(), thresh=15, conf=0.5)
        cv2.imshow("img_out", img_out)
        perspective = self.vision_func(frame=frame)
        self.angle = self.angele(frame=perspective)
        cv2.imshow("perspective", perspective)
        print(svet_sign)
        # stop_line = self.detect_stop_line(frame=perspective)
        # if stop_line:
        #     print("STOP_LINE")
        #     self.speed = 1500
        #     self.stopeer_f()
        # if self.need_svet == True:
        #     if svet_sign == "green":
        #         self.speed = speed
        #     else:
        #         self.speed = 1500
        # send_cmd('H00/' + str(speed) + '/' + str(angle) + "E")
        # else:
        # send_cmd('H00/' + '1450' + '/' + str(angle) + "E")
        # time.sleep(0.5)
        # send_cmd('H00/' + str(stop_speed) + '/' + str(angle) + "E")
        return self.angle, self.speed


class VisionPovorots:
    def __init__(self, go=None, d=0):
        # go - Список как еме ехать после перекрестка
        self.d = d
        self.last = 0
        self.angle_pd = PD(kP=KP, kD=KD)
        self.speed = speed
        self.exit = False
        self.pov = 0
        self.r = 0
        self.l = 0
        self.Go = go
        self.nGo = len(go) if self.Go is not None else -1
        self.kGo = 0
        self.timeLast = 0
        self.next = 0
        self.speedPovorot = 1550

    def resetPeret(self):
        self.next = 0
        self.timeLast = 0
        self.kGo = self.kGo + 1 if self.kGo + 1 < self.nGo else 0
        self.pov = 0
        self.exit = False
        self.l = 0
        self.r = 0

    def vision_func(self, frame):
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

    def angele(self, left, right):
        # image = frame.copy()
        # left, right = centre_mass(image, d=self.d)
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
        left, right = centre_mass(perspective.copy())
        if self.exit:
            self.speed = speed
        cv2.imshow("perspective", perspective)
        if self.pov == 0:  # проверка едит ли он по полигону, или он на перекрестке
            self.angle = self.angele(left=left, right=right)
            stop_line = self.detect_stop_line(frame=perspective)
            if stop_line:
                self.angle = 87
                print("STOP_LINE")
                self.speed = 1450
                self.stopeer_f()
                self.pov = 1
                if self.nGo != -1:
                    self.l, self.r = (1, 0) if self.Go[self.kGo] == 'l' else (0, 1) if self.Go[self.kGo] == 'r' else (
                    1, 1)
        elif self.exit:
            if self.l == 1 and self.r == 1:  # ехать прямо
                if left >= 150 and self.next == 0:
                    self.next += 1
                elif left < 150 and self.next == 1:
                    self.next += 1
                if self.next <= 1:
                    self.angle = 87
                else:
                    self.resetPeret()
            elif self.l == 1:
                self.speed = self.speedPovorot
                if self.timeLast == 0:
                    self.timeLast = time.time()
                else:
                    if time.time() - self.timeLast >= 1 and self.next == 0:
                        self.next += 1
                        self.timeLast = 0
                    elif time.time() - self.timeLast >= 3.5 and self.next == 1:
                        self.next += 1
                    if self.next == 0:
                        self.angle = 88
                    elif self.next == 1:
                        self.angle = 87 + 28
                    else:
                        self.resetPeret()
                    print("Left = ", time.time() - self.timeLast, "angle = {} speed = {}".format(self.angle, self.speed))
            elif self.r == 1:
                if self.timeLast == 0:  # По времени
                    self.timeLast = time.time()
                else:
                    if time.time() - self.timeLast >= 0.5 and self.next == 0:
                        self.next += 1
                    elif time.time() - self.timeLast >= 2.5 and self.next == 1:
                        self.next += 1
                    if self.next == 0:
                        self.angle = 87
                    elif self.next == 1:
                        self.angle = 87 - 30
                    else:
                        self.resetPeret()

        return self.angle, self.speed
