#!/usr/bin/env python3

import cv2
import beholder
import numpy as np
import socket
import time

from func import *
from TaskClasses import *

def send_cmd(cmd):
    message = cmd.encode()
    sock.sendall(message)


DEFAULT_CMD = 'H11/1500/90E'

def povorotRight():
    # control(pi, ESC, 1550, STEER, 90) - # На право по времени
    # time.sleep(0.6)
    # control(pi, ESC, 1550, STEER, 90 - 25)
    # time.sleep(1)

    angle_pd = PD(kP=KP, kD=KD)
    ret, frame = cap.read()
    frame_copy = frame.copy()
    perspective = vision.vision_func(frame=frame_copy)
    angle = vision.angele(frame=perspective.copy())
    left, right = centre_mass(perspective.copy())
    send_cmd('H00/' + str(speed) + '/' + str(angle) + "E")
    while left < 150:
        ret, frame = cap.read()
        frame_copy = frame.copy()
        perspective = vision.vision_func(frame=frame_copy)
        angle = vision.angele(frame=perspective.copy())
        left, right = centre_mass(perspective.copy())
    while left >= 150:
        ret, frame = cap.read()
        frame_copy = frame.copy()
        perspective = vision.vision_func(frame=frame_copy)
        left, right = centre_mass(perspective.copy())
        angle = angle_pd.calc(left=115, right=right)
        if angle < 70:
            angle = 70
        elif angle > 106:
            angle = 104
        send_cmd('H00/' + str(speed) + '/' + str(angle) + "E")

def forward():
    ret, frame = cap.read()       #  Ехать прямо, Пока не видит линию с лева
    frame_copy = frame.copy()
    perspective = vision.vision_func(frame=frame_copy)
    left, right = centre_mass(perspective.copy())
    while left < 150:
        ret, frame = cap.read()
        frame_copy = frame.copy()
        perspective = vision.vision_func(frame=frame_copy)
        left, right = centre_mass(perspective.copy())
        send_cmd('H00/' + str(speed) + '/' + str(90) + "E")
    while left >= 150:
        ret, frame = cap.read()
        frame_copy = frame.copy()
        perspective = vision.vision_func(frame=frame_copy)
        left, right = centre_mass(perspective.copy())
        send_cmd('H00/' + str(speed) + '/' + str(90) + "E")

    # send_cmd('H00/' + str(speed) + '/' + str(90) + "E")
    # wait_time(time_wait=3)#Едет 3 секунды

    # encoders = 0    #В этой перемене будет находиться энкодеры самой машинки
    # encoders_forward = 200
    # while encoders <= encoders_forward:
    #     # send_cmd('H00/' + str(speed) + '/' + str(90) + "E")


def pororotLeft():
    end_cmd('H00/' + str(speed) + '/' + str(90) + "E") # на лево по времени
    time.sleep(0.9)
    end_cmd('H00/' + str(speed) + '/' + str(90+25) + "E")
    time.sleep(0.9)

# Connection with raspberry to transmit commands
sock = socket.socket()
server_address = (IPadress, 1080)
sock.connect(server_address)
print("Connection Established")

# Request a video stream from Eyecar
client = beholder.Client(zmq_host=IPadress,
                         # zmq_host="192.168.1.145",
                         zmq_port=12345,
                         rtp_host="192.168.1.208",
                         # rtp_host="10.205.1.185",
                         rtp_port=5000,
                         rtcp_port=5001,
                         device="/dev/video0",
                         # width=1920,
                         # height=1080,
                         width=1280,
                         height=720,
                         # width=640,
                         # height=480,
                         framerate=30,
                         encoding=beholder.Encoding.MJPEG,  # MJPEG,    #H264
                         limit=20)

client.start()

#
cv2.namedWindow("Frame")

send_cmd(DEFAULT_CMD)

vision = Vision()
go = ['f', 'l', 'r', 'r', 'f', 'l']
nGo = 6
kGo = 0
while cv2.waitKey(10) != ESCAPE:
    status, frame = client.get_frame(0.25)  # read the sent frame
    if status == beholder.Status.OK:
        cv2.imshow("Frame", frame)
        frame_copy = frame.copy()
        perspective = vision.vision_func(frame=frame_copy)
        angle = vision.angele(frame=perspective)
        stop_line = vision.detect_stop_line(frame=perspective)

        if not stop_line:
            send_cmd('H00/' + str(spd) + '/' + str(ang) + "E")
        else:
            send_cmd('H00/' + '1450' + '/' + str(ang) + "E")
            time.sleep(0.5)
            send_cmd('H00/' + str(spd) + '/' + str(ang) + "E")
            if go[kGo] == 'f':
                forward()
            elif go[kGo] == 'r':
                povorotRight()
            elif go[kGo] == 'l':
                pororotLeft()
            kGo += 1
            if kGo >= nGo:
                kGo = 0
            

        key = cv2.waitKey(1)

    elif status == beholder.Status.EOS:
        print("End of stream")
        break
    elif status == beholder.Status.Error:
        print("Error")
        break
    elif status == beholder.Status.Timeout:
        # Do nothing
        pass

# Completion of work
send_cmd(DEFAULT_CMD)  # Stop the car
sock.close()
cv2.destroyAllWindows()
client.stop()
