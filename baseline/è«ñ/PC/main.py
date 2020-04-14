#!/usr/bin/env python3

import cv2
import beholder
import numpy as np
import socket
import time

from func import *


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

#
cv2.namedWindow("Frame")

send_cmd(DEFAULT_CMD)

vision = Vision()

while cv2.waitKey(10) != ESCAPE:
    status, frame = client.get_frame(0.25)  # read the sent frame
    if status == beholder.Status.OK:
        cv2.imshow("Frame", frame)
        frame_copy = frame.copy()
        perspective = vision.vision_func(frame=frame_copy)
        angle = vision.angele(frame=perspective)
        stop_line = vision.detect_stop_line(frame=perspective)
#         stop_line = detect_stop(perspective)

        if not stop_line:
            send_cmd('H00/' + str(speed) + '/' + str(angle) + "E")
        else:
            send_cmd('H00/' + '1450' + '/' + str(angle) + "E")
            time.sleep(0.5)
            send_cmd('H00/' + str(stop_speed) + '/' + str(angle) + "E")
            

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
