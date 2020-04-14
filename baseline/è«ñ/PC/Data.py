import numpy 
import cv2

import json
import time
# from DataDefault import default
# from DataDefault import gen_default
# FLOAT_PRINT_RES

class DataField:
    def __init__(self, time=0, data="", name=""):
        self.name = name
        self.time = time
        self.data = data
        self.default = True
    def __str__(self):
        outt = str(round(self.time, 3))
        if "." in outt:
            if len(outt.split(".")[1]) < 3:
                outt += "0"
        return  "def:" + str(self.default) + " t:" + str(outt) + " data:" + str(self.data) 
        # else:
        #     out = str(round(self.data, 3))
        #     if len(out) < 3+1+1:
        #         out += "0"
        #     return "def:" + str(self.default)  + " t:" + str(self.time) + " data:" + out 


def gen_default(din):
    d = dict(din)
    for i in d.keys():
        d[i] = DataField(time=0, data=d[i], name=i)
    return d

class DataControl:
    def __init__(self, path="./configs/data_cfg.json"):
        
        self.st_time = 0 
        self.data = gen_default(json.load(open(path, "r"))["default"])
    def start(self):
        self.st_time = time.time()
    def set(self, field_name, field_data):
        t_now = time.time() - self.st_time 
        
        if  field_name in self.data.keys():
            self.data[field_name].time = round(t_now, 3)
            self.data[field_name].data = field_data
            self.data[field_name].default = False
            return t_now
        else:
            return -1
    def get(self, field_name) -> DataField :
        if  field_name in self.data.keys():
            d = self.data[field_name]
            return  d
        else:
            return DataField()
    def __str__(self):
        # return str(self.data)
        out = ""
        for i in self.data.keys():
            out += "" + i + ":\n"
            out += "  " + str(self.data[i]) + "\n"
        return str(out)