import numpy as np 
import Data
import threading

import Utils
import PID

import json

from DriveScripts.StopSign import StopSign
from DriveScripts.PedestrianSign import PedestrianSign
class Drive:
    def __init__(self, drive_data: Data.DataControl):
        self.drive_data = drive_data
        self.config = json.load(open("./configs/drive_cfg.json", "r"))
        self.drive_data.set("std_speed", self.config.std_speed)
        self.pid = PID.PID(kP=self.config.PID.p, kI=self.config.PID.i, kD=self.config.PID.d)
        self.stop_script = StopSign(self.config.scripts["stop_sign"], self.drive_data)
        self.pedestrian_script = PedestrianSign(self.config.scripts["pedestrian_sign"], self.drive_data)
        print("DRIVE", self.config)
    def run(self):
        e1_d = self.drive_data.get(Utils.E1)
        e2_d = self.drive_data.get(Utils.E2)
        
        if self.config.scripts["stop_sign"].enable == True:
            self.stop_script.run()
        if self.config.scripts["pedestrian_sign"].enable == True:
            self.pedistrain_script.run()
        
        pid_r = self.pid.calc(e1_d.data*self.config.e1_K + e2_d.data*self.config.e2_K)
        self.drive_data.set("servo", pid_r+self.config.std_servo)



