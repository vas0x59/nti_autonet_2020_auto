import Data
import numpy as np
from obj_detectors.Detectors.YoloOpencvDetector import YoloOpencvDetector
from obj_detectors.Detectors import Utils
import cv2
cv = cv2
def get_area(p):
    return p[2]*p[3]


class OBJDetection:
    def __init__(self):
        # self.drive_data = drive_data
        self.detector = None
        self.detector_std = None
        # self.model_w_path = "yolo_sign_model_v1/yolov3_signs_v1_12800.weights"
        # self.model_c_path = "yolo_sign_model_v1/yolov3_signs_v1.cfg"
        # self.model_n_path = "yolo_sign_model_v1/signs.names"
        self.model_w_path = "yolo_sign_v2/yolov3_cfg_81000.weights"
        self.model_c_path = "yolo_sign_v2/yolov3_cfg.cfg"
        self.model_n_path = "yolo_sign_v2/classes.txt"
        self.model_res = 320
        self.sings_filter = ["pedestrian", "stop", "parking",
                             "a_unevenness", "road_works", "way_out", "no_drive", "no_entery"]
        self.filter_dict = dict().fromkeys(self.sings_filter, 0)
        self.frames_left = 0
        self.hist = []
        self.labels = ['red', 'yellow', 'green']
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
        self.detector = YoloOpencvDetector(
            self.model_c_path, self.model_w_path, CLASSESPath=self.model_n_path)
        # self.detector_std = YoloOpencvDetector("obj_detectors/Detectors/YOLO/yolov3_tiny.cfg",
        #                                        "obj_detectors/Detectors/YOLO/yolov3_tiny.weights", CLASSESPath="obj_detectors/coco.names")

    def predict_svet(self, inm):
        crop2 = inm.copy()
        est = False
        svet = [0, 0, 0]
        h, w = crop2.shape[:2]
        # q = crop.copy()
        # crop2 = cv.cvtColor(crop2, cv.COLOR_RGB2BGR)

        # svezt[3] = 3
        cv2.imshow("1", crop2)
        crop2 = cv.cvtColor(crop2, cv.COLOR_BGR2HLS)[:, :, 1]
        # crop2 = cv.inRange(crop2, (0, 80, 180), (255, 255, 255))
        # crop2 = crop2[:, :, 2]s
        crop2 = cv.medianBlur(crop2, 3)
        cv2.imshow("crop2", crop2)
        redCrop = crop2[int(h// 15):h//15*4]
        yellowCrop = crop2[h//15*5:h//15*9]
        greenCrop = crop2[h//15*10:int(h// 15 * 14)]
        # cv2.imshow("cr", crop2)
        # cv2.waitKey(1)
        # svet[0] = np.sum(redCrop[:,:,2]) / (w*h)
        # redBlueSum = np.sum(redCrop[:,:,0]) / (w*h)
        svet[0] = np.mean(redCrop[:, :]) / float(255)

        # svet[1] = (np.sum(yellowCrop[:,:,1]) + np.sum(yellowCrop[:,:,2]))/2 / (w*h)
        # yellowBlueSum = np.sum(yellowCrop[:,:,0]) / (w*h)
        svet[1] = np.mean(yellowCrop[:, :]) / float(255)
        # svet[2] = np.sum(greenCrop[:,:,1]) / (w*h)
        svet[2] = np.mean(greenCrop[:, :]) / float(255)
        # if (abs(svet[0]-svet[2]) < 0.05):
        #     return "yellow"
        # print(svet)
        # return self.labels[svet.index(max(svet))]
        label = "none"
        print(svet)
        if max(svet) > 0.5:
            if svet[0] > svet[2] and svet[1] > svet[2] and svet[0] > 0.55 and svet[1] > 0.55 :
                label = "red_yellow"
            elif svet[2]*1 > svet[0] and svet[2]*1 > svet[1]:
                label = "green"
            elif svet[1] > svet[2] and svet[1] > svet[0]:
                label = "yellow"
            elif svet[0] > svet[2] and svet[0] > svet[1]:
                label = "red"
        return label


    def run(self, frame, thresh=6, conf=0.5):
        frame = frame[:, frame.shape[1] // 2:]
        boxes, classIDs, confidences = self.detector.detect(
            frame, s=(self.model_res, self.model_res), conf=conf)
        img_out = Utils.draw_boxes(
            frame, boxes, classIDs, confidences, self.detector.CLASSES, COLORS=self.detector.COLORS)

        signs_o = sorted([(self.detector.CLASSES[classIDs[i]], boxes[i]) for i in range(len(classIDs)) if get_area(boxes[i]) > frame.shape[0]
                          * frame.shape[1] * 0.01 and self.detector.CLASSES[classIDs[i]] in self.sings_filter], key=lambda x: get_area(x[1]), reverse=True)
        # print(signs_o)
        signs = [i[0] for i in signs_o]
        # self.drive_data.set("signs", signs)
        svet_label = "none"
        if "traffic_light" in [self.detector.CLASSES[i] for i in classIDs]:
            svet = max([(confidences[i], boxes[i]) for i in range(len(
                classIDs)) if self.detector.CLASSES[classIDs[i]] == "traffic_light"], key=lambda x: x[0])[1]
            # svet = svet
            svet_label = self.predict_svet(frame[np.clip(svet[1], 0, frame.shape[0]):np.clip(
                svet[1] + svet[3], 0, frame.shape[0]), np.clip(svet[0], 0, frame.shape[1]):np.clip(svet[0] + svet[2], 0, frame.shape[1])])
        print(svet_label)
        # boxes, classIDs, confidences = self.detector_std.detect(
        #     frame, s=(self.model_res, self.model_res))
        # img_out = Utils.draw_boxes(img_out, boxes, classIDs, confidences,
        #                            self.detector_std.CLASSES, COLORS=self.detector_std.COLORS)
        # for i in signs:
        # self.filter_dict[i] += 1
        # if self.frames_left == thresh:
        # self.frames_left = 0
        # self.filter_dict = dict().fromkeys(self.sings_filter, 0)
        # else:
        # self.frames_left +=1

        mm = "none"
        self.hist += signs
        if len(self.hist) > thresh:
            self.hist = self.hist[thresh:]
        self.filter_dict = dict().fromkeys(self.sings_filter, 0)
        for i in self.hist:
            self.filter_dict[i] += 1
        if sum(map(lambda x: x[1], self.filter_dict.items())) > 0 and len(self.hist) > 4:
            mm = max(self.filter_dict.items(), key=lambda x: x[1])[0]
        return img_out, signs, mm
