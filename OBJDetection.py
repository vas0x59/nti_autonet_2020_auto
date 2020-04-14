import Data
import numpy as np
from obj_detectors.Detectors.YoloOpencvDetector import YoloOpencvDetector
from obj_detectors.Detectors import Utils 

def get_area(p):
    return p[2]*p[3]

class OBJDetection:     
    def __init__(self):
        # self.drive_data = drive_data
        self.detector = None
        self.detector_std = None
        self.model_w_path = "yolo_sign_model_v1/yolov3_signs_v1_12800.weights"
        self.model_c_path = "yolo_sign_model_v1/yolov3_signs_v1.cfg"
        self.model_n_path = "yolo_sign_model_v1/signs.names"
        self.model_res = 320
        self.sings_filter = ["pedestrian", "stop", "parking", "a_unevenness", "road_works", "way_out", "no_drive", "no_entery"]
        self.filter_dict = dict().fromkeys(self.sings_filter, 0)
        self.frames_left = 0
        """
        pedestrian
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

    def run(self, frame, thresh=6):
        frame = frame[:, frame.shape[1] // 2:]
        boxes, classIDs, confidences = self.detector.detect(frame, s=(self.model_res, self.model_res))
        img_out = Utils.draw_boxes(frame, boxes, classIDs, confidences, self.detector.CLASSES, COLORS=self.detector.COLORS)
        signs_o = sorted([(self.detector.CLASSES[classIDs[i]], boxes[i])  for i in range(len(classIDs))], key=lambda x:get_area(x[1]), reverse=True)
        # print(signs_o)
        signs = [i[0] for i in signs_o]
        # self.drive_data.set("signs", signs)

        boxes, classIDs, confidences = self.detector_std.detect(frame, s=(self.model_res, self.model_res))
        img_out = Utils.draw_boxes(img_out, boxes, classIDs, confidences, self.detector_std.CLASSES, COLORS=self.detector_std.COLORS)
        for i in signs:
            self.filter_dict[i] += 1
        if self.frames_left == thresh:
            self.frames_left = 0
            self.filter_dict = dict().fromkeys(self.sings_filter, 0)
        else:
            self.frames_left +=1
            
        mm = "none"
        if sum(map(lambda x: x[1], self.filter_dict.items())) > 0:
            mm = max(self.filter_dict.items(), key=lambda x: x[1])[0]
        return img_out, signs, mm
