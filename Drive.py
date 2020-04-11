import numpy as np 
import Data
import threading

import Utils
import PID

import json

class Drive:
    def __init__(self, drive_data: Data.DataControl):
        self.drive_data = drive_data
        self.config = json.load(open("./configs/drive_cfg.json", "r"))

    def run(self):
        e1_d = self.drive_data.get(Utils.E1)
        e2_d = self.drive_data.get(Utils.E2)
        signs_d = self.drive_data.get(Utils.SIGNS_LIST)
        if self.config.scripts["stop_sign"].enable == True:
            self.stop_script()
        
        # if self.drive_data.get("objd").data ==    
        # e1_e.data
    
    def stop_script(self):
        pass

    def 


