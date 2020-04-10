import Data
import numpy as np
from obj_detectors.Detectors.YoloOpencvDetector import YoloOpencvDetector
from obj_detectors.Detectors import Utils 

def get_area(p):
    return p[2]*p[3]

class OBJDetection:     
    def __init__(self, drive_data: Data.DataControl):
        self.drive_data = drive_data
        self.detector = None
        self.detector_std = None
        self.model_w_path = "yolo_sign_model_v1/yolov3_signs_v1_12800.weights"
        self.model_c_path = "yolo_sign_model_v1/yolov3_signs_v1.cfg"
        self.model_n_path = "yolo_sign_model_v1/signs.names"
        self.model_res = 320
        self.sings_filter = ["pedistrain", "stop", "parking"]
        """
        pedistrain
        no_drive
        a_unevenness
        no_entery
        road_works
        stop
        way_out
        parking
        """
    def load(self):
        self.detector = YoloOpencvDetector(self.model_c_path, self.model_w_path, CLASSESPath=self.model_n_path)
        self.detector_std = YoloOpencvDetector("obj_detectors/Detectors/YOLO/yolov3_tiny.cfg", "obj_detectors/Detectors/YOLO/yolov3_tiny.weights", CLASSESPath="obj_detectors/coco.names")

    def run(self, frame):
        boxes, classIDs, confidences = self.detector.detect(frame, s=(self.model_res, self.model_res))
        img_out = Utils.draw_boxes(frame, boxes, classIDs, confidences, self.detector.CLASSES, COLORS=self.detector.COLORS)
        signs_o = sorted([(self.detector.CLASSES[classIDs[i]], boxes[i])  for i in range(len(classIDs)) if self.detector.CLASSES[classIDs[i]] in self.sings_filter], key=lambda x:get_area(x[1]), reverse=True)
        # print(signs_o)
        signs = [i[0] for i in signs_o]
        self.drive_data.set("signs", signs)

        boxes, classIDs, confidences = self.detector_std.detect(frame, s=(self.model_res, self.model_res))
        img_out = Utils.draw_boxes(img_out, boxes, classIDs, confidences, self.detector_std.CLASSES, COLORS=self.detector_std.COLORS)

        return img_out
