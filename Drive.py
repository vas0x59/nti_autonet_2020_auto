import numpy as np 
import Data
import threading

import Utils
import PID

class Drive:
    def __init__(self, drive_data: Data.DataControl):
        self.drive_data = drive_data

    def run(self):
        e1_d = self.drive_data.get(Utils.E1)
        e2_d = self.drive_data.get(Utils.E2)
        # e1_e.data







