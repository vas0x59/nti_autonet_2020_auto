#!/usr/bin/env python3

import cv2
import beholder
import numpy as np
import socket
import time

from func import *
from TaskClass2 import *


def send_cmd(cmd):
    message = cmd.encode()
    sock.sendall(message)


DEFAULT_CMD = 'H11/1500/90E'

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


cv2.namedWindow("Frame")

send_cmd(DEFAULT_CMD)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
status, frame = client.get_frame(0.25)
out = cv2.VideoWriter('output_' + str(int(time.time())) + '.avi', fourcc, 28.0, (frame.shape[1], frame.shape[0]))

vision = Vision()

while cv2.waitKey(10) != ESCAPE:
    status, frame = client.get_frame(0.25)  # read the sent frame
    if status == beholder.Status.OK:
        cv2.imshow("Frame", frame)
        out.write(frame)

        ang, spd = vision.run(frame.copy())

        send_cmd('H00/' + str(spd) + '/' + str(ang) + "E")


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
out.release()

if hasattr(vison, 'client'):
    vision.client.loop_stop(force=False)