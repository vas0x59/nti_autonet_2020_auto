from func import *
from OBJDetection import OBJDetection
import paho.mqtt.client as mqtt
import time


class Vision:
    def __init__(self, d=0):
        self.d = d
        self.last = 0
        self.angle_pd = PD(kP=KP, kD=KD)
        self.speedPovorot = 1550
        self.speed = speed
        self.exit = False
        self.need_svet = False
        self.objd = OBJDetection()
        self.signs = []
        self.sign = "none"
        self.sign_hist = []
        self.objd.load()
        self.timeLast = 0
        self.l = 0
        self.r = 0
        self.pov = 0
        self.go = 0
        self.next = 0
        self.timeNow = 0
        self.kyda = []  # Здесь будут хранится куда ему надо будет поварачиваться, после каждого пройденого маршрута, этот элемент будет удалаться
        self.nKyda = len(self.kyda)  # Количество маршрутов
        self.objd.svet_enable = False
        self.objd.sign_enable = True
        self.signStop = 0
        self.angle = 87
        # self.client = mqtt.Client()
        # self.client.on_connect = self.on_connect
        # self.client.on_message = self.on_message
        # self.client.connect("192.168.1.208", 1883, 60)
        # self.client.loop_start()
        time.sleep(1)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("/dispatcher/truck")

    def on_message(self, client, userdata, msg):
        data = str(msg.payload.decode("utf-8"))
        print(msg.topic + " " + str(data))
        # data = str(msg.payload)
        # var += list(var)
        klocal = list(data.split())
        klocal = map(str.lower, klocal)

        self.kyda += list(klocal)
        self.nKyda = len(self.kyda)

    def resetPeret(self):
        self.need_svet = False
        self.next = 0
        self.go = 0
        self.pov = 0
        self.timeNow = 0
        del self.kyda[0]
        self.nKyda = len(self.kyda)
        self.l = 0
        self.r = 0
        self.signStop = 0
        self.objd.svet_enable = False
        self.objd.sign_enable = True

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
        self.need_svet = True

    def run(self, frame):
        # if self.objd.sign_enable:
        img_out, ssnow, self.sign, svet_sign, person = self.objd.run(frame.copy(), conf=0.05)
        cv2.imshow("img_out", img_out)
        if person:
            self.speed = 1500
            self.stopeer_f()
            return self.angle, self.speed
        if self.signStop == 0:
            if self.sign == 'stop':
                self.speed = 1500
                if self.timeLast == 0:
                    self.timeLast = time.time()
                elif time.time() - self.timeLast > 5:
                    self.signStop = 1
                    self.speed = speed
                    self.timeLast = 0
                return self.angle, self.speed
        perspective = self.vision_func(frame=frame.copy())
        left, right = centre_mass(perspective.copy())
        cv2.imshow("perspective", perspective)
        if self.pov == 0:
            self.need_svet = False
            stop_line = self.detect_stop_line(frame=perspective)
            if stop_line:
                self.objd.svet_enable = True
                self.objd.sign_enable = False
                print("STOP_LINE")
                self.angle = 88
                self.speed = 1500
                self.stopeer_f()
                self.pov = 1
                if self.nKyda > 0:
                    self.l, self.r = (1, 0) if self.kyda[0] == 'l' else (0, 1) if self.kyda[0] == 'r' else (1, 1)
                else:
                    self.speed = 1500
            else:
                self.angle = self.angele(left=left, right=right)
        else:
            if self.go == 0:
                # img_out, ssnow, self.sign, svet_sign, person = self.objd.run(frame.copy(), thresh=15, conf=0.5)
                if self.need_svet:
                    if svet_sign == "green":
                        self.go = 1
                        self.angle = 88
                        self.speed = speed
                    else:
                        self.go = 0
                        self.speed = stop_speed
            else:
                if self.l == 1 and self.r == 1:  # ехать прямо
                    if left >= 150 and self.next == 0:
                        self.next += 1
                    elif left < 150 and self.next == 1:
                        self.next += 1
                    if self.next <= 1:
                        self.angle = 88
                    else:
                        self.resetPeret()
                elif self.l == 1:  # Ехать на лево
                    self.speed = self.speedPovorot
                    if self.timeLast == 0:  # По времени
                        self.timeLast = time.time()
                    else:
                        if time.time() - self.timeLast >= 0.9 and self.next == 0:
                            self.next += 1
                            self.timeLast = 0
                        elif time.time() - self.timeLast >= 3.5 and self.next == 1:
                            self.next += 1
                        if self.next == 0:
                            self.angle = 88
                        elif self.next == 1:
                            self.angle = 88 + 25
                        else:
                            self.resetPeret()
                elif self.r == 1:  # ехать на право
                    self.speed = speed
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
