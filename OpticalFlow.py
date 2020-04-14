import cv2
import numpy as np 
cv = cv2
import time
import Data
class OpticalFlow:
    def __init__(self, drive_data: Data.DataControl):
        self.feature_params = dict( maxCorners = 75,
                       qualityLevel = 0.5,
                       minDistance = 5,
                       blockSize = 5 )
        # Parameters for lucas kanade optical flow
        self.lk_params = dict( winSize  = (15,15),
                        maxLevel = 2,
                        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))        
        self.prev_frame = None
        self.p0 = []
        self.pr_t = time.time()
        self.drive_data = drive_data
    # def optical_flow(self):
    def estimate_motion(self, g0, g1):
        now_h = cv2.convertPointsToHomogeneous(g1)
        prev_h = cv2.convertPointsToHomogeneous(g0)
        # print("test", now_h, self.p1)
        motion_avg = np.array((0, 0, 0), dtype="float")
        if prev_h is not None:
            n = len(prev_h)
            if n > 0:
                for i in range(n):
                    motion_avg += (now_h[i][0] - prev_h[i][0]) / n
        t = time.time() - self.pr_t
        self.pr_t = time.time()
        sh = self.frame.shape
        motion_avg[0] /= sh[1]
        motion_avg[1] /= sh[0]
        return motion_avg / t


    def run(self, frame):
        img_out = frame.copy()
        if self.prev_frame is None or self.p0 is None or len(self.p0) <= 0:
            self.prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.p0 = cv.goodFeaturesToTrack(self.prev_frame, mask = None, **self.feature_params)
        else:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.p1, st, err = cv2.calcOpticalFlowPyrLK(self.prev_frame, self.frame, self.p0, None, **self.lk_params)
            good_new = self.p1[st==1]
            good_old = self.p0[st==1]
            em = self.estimate_motion(good_old, good_new)
            self.drive_data.set("opt_x", em[0])
            self.drive_data.set("opt_y", em[1])
            self.prev_frame = self.frame.copy()
            if self.p0 is None or len(self.p0) < self.feature_params["maxCorners"]*0.1:
                self.p0 = cv.goodFeaturesToTrack(self.frame, mask = None, **self.feature_params)
            else:
                self.p0 = good_new.reshape(-1,1,2)
            # if not self.p0 is None:
            #     print(len(self.p0))
            
            # img_out = 
            for i,(new,old) in enumerate(zip(good_new, good_old)):
                a,b = new.ravel()
                c,d = old.ravel()
                img_out = cv.circle(img_out,(c,d),5,(255, 255, 0),-1)
                img_out = cv.circle(img_out,(a,b),5,(0, 255, 0),-1)
        return img_out