import cv2
import numpy as numpy
import time 
import 

class LANEDetection:
    def __init__(self, drive_data: Data.DataControl, img_size = [200, 360]):
        self.drive_data = drive_data
        self.img_size = img_size
        self.points = []

        self.clip_value = 100
        self.nwindows = 8
        self.window_half_width = 60
        # self.src = np.float32([[20, 200],
        #           [350, 200],
        #           [275, 120],
        #           [85, 120]])
        # self.src = np.float32([[10, 200],
        #           [350, 200],
        #           [275, 120],
        #           [85, 120]])
        # self.src = np.float32([[0, 200],
        #           [360, 200],
        #           [310, 120],
        #           [50, 120]])

        #good
        # self.src = np.float32([[0, 200],
        #           [360, 200],
        #           [310, 120],
        #           [50, 120]])

        # self.src = np.float32([[0, 200],
        #           [360, 200],
        #           [300, 100],
        #           [60, 100]])

        self.src = np.float32([[0, 200],
                  [360, 200],
                  [300, 120],
                  [60, 120]])

        # self.src = np.float32([[0, 299],
        #            [399, 299],
        #            [320, 200],
        #            [80, 200]])

        self.src_draw=np.array(self.src,dtype=np.int32)

        self.dst = np.float32([[0, img_size[0]],
                        [img_size[1], img_size[0]],
                        [img_size[1], 0],
                        [0, 0]])
    
    def run(self, frame: np.array):
        frame = frame.copy()
        # frame.
        frame = self.warp(frame)
        frame = self.thresh(frame)
        points, out_img = self.detect(frame)
        return out_img
        
    def warp(self, img):
        M = cv2.getPerspectiveTransform(self.src, self.dst)
        warped = cv2.warpPerspective(img, M, (self.img_size[1],self.img_size[0]), flags=cv2.INTER_LINEAR)
        return warped

    def thresh(self, img):
        img[(img < self.clip_value)] = self.clip_value
        # cv2.clip
        img_blur = cv2.medianBlur(img, 5)
        # if show==True:
        #     cv2.imshow("warpedq",img_blur)
        # cv2.imshow("warped1",warped)
        # warped = cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        #     cv2.THRESH_BINARY_INV,5,2)
        
        img = cv2.adaptiveThreshold(img_blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY_INV,5,2)

        # element = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        # kernel = np.ones((10,10),np.uint8)
        img = cv2.erode(img, np.ones((1,1),np.uint8))
        # warped = cv2.dilate(warped,np.ones((1,1),np.uint8),iterations = 1)
        # warped = 
        # warped = self.thresh(warped)
        # warped = cv2.morphologyEx(warped, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
        img = cv2.medianBlur(img, 3)
        return img
    def detect(self, img):
        histogram = np.sum(warped[warped.shape[0]//2:,:],axis=0)

        midpoint = histogram.shape[0]//2
        IndWhitestColumnL = np.argmax(histogram[:midpoint])
        IndWhitestColumnR = np.argmax(histogram[midpoint:])+midpoint
        warped_visual = warped.copy()
        # if show==True:
        #     cv2.line(warped_visual, (IndWhitestColumnL,0), (IndWhitestColumnL,warped_visual.shape[0]), 110, 2)
        #     cv2.line(warped_visual, (IndWhitestColumnR, 0), (IndWhitestColumnR, warped_visual.shape[0]), 110, 2)
        #     cv2.imshow("WitestColumn",warped_visual)

        
        window_height = np.int(warped.shape[0]/self.nwindows)
        

        XCenterLeftWindow = IndWhitestColumnL
        XCenterRightWindow = IndWhitestColumnR

        left_lane_inds = np.array([],dtype=np.int16)
        right_lane_inds = np.array([], dtype=np.int16)

        out_img = np.dstack((warped, warped, warped))

        nonzero = warped.nonzero()
        WhitePixelIndY = np.array(nonzero[0])
        WhitePixelIndX = np.array(nonzero[1])

        for window in range(self.nwindows):

            win_y1 = warped.shape[0] - (window+1) * window_height
            win_y2 = warped.shape[0] - (window) * window_height

            left_win_x1 = XCenterLeftWindow - self.window_half_width
            left_win_x2 = XCenterLeftWindow + self.window_half_width
            right_win_x1 = XCenterRightWindow - self.window_half_width
            right_win_x2 = XCenterRightWindow + self.window_half_width

            if show==True:
                cv2.rectangle(out_img, (left_win_x1,win_y1),(left_win_x2,win_y2),(50 + window *21,0,0),2)
                cv2.rectangle(out_img, (right_win_x1, win_y1), (right_win_x2, win_y2), (0, 0, 50 + window * 21), 2)
                # cv2.imshow("windows",out_img)

            good_left_inds = ((WhitePixelIndY>=win_y1) & (WhitePixelIndY<=win_y2) &
            (WhitePixelIndX >= left_win_x1) & (WhitePixelIndX <= left_win_x2)).nonzero()[0]

            good_right_inds = ((WhitePixelIndY >= win_y1) & (WhitePixelIndY <= win_y2) &
                            (WhitePixelIndX >= right_win_x1) & (WhitePixelIndX <= right_win_x2)).nonzero()[0]

            left_lane_inds = np.concatenate((left_lane_inds,good_left_inds))
            right_lane_inds = np.concatenate((right_lane_inds, good_right_inds))

            if len(good_left_inds) > 50:
                XCenterLeftWindow = np.int(np.mean(WhitePixelIndX[good_left_inds]))
            if len(good_right_inds) > 50:
                XCenterRightWindow = np.int(np.mean(WhitePixelIndX[good_right_inds]))

        if show==True:
            out_img[WhitePixelIndY[left_lane_inds],WhitePixelIndX[left_lane_inds]]=[255,0,0]
            out_img[WhitePixelIndY[right_lane_inds], WhitePixelIndX[right_lane_inds]] = [0, 0, 255]
        
        #     cv2.imshow("Lane",out_img)

        leftx=WhitePixelIndX[left_lane_inds]
        lefty = WhitePixelIndY[left_lane_inds]
        rightx = WhitePixelIndX[right_lane_inds]
        righty = WhitePixelIndY[right_lane_inds]
        center_fit = []
        points = []
        if (len(lefty) > 10) and (len(leftx) > 10) and (len(righty) > 10) and (len(rightx) > 10):
            left_fit=np.polyfit(lefty,leftx,2)
            right_fit=np.polyfit(righty, rightx, 2)

            center_fit = ((left_fit+right_fit)/2)
            points = []
            for ver_ind in range(out_img.shape[0]):
                gor_ind = ((center_fit[0]) * (ver_ind ** 2) +
                            center_fit[1] * ver_ind +
                            center_fit[2])
                
                # cv2.circle(out_img,(int(gor_ind),int(ver_ind)),2,(255,0,255),1)
                points.append([gor_ind, ver_ind])
        return points, out_img