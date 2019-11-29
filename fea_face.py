#coding=utf-8
import numpy as np
from xlrd import open_workbook
import face_recognition
import cv2
import math
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import pandas as pd


class face_fea():
    def __init__(self, filename):
        """
        :param filename: 需要处理的文件名
        """
        self.filename = filename
        self.data = {}
        self.farr = []
        self.zs = 0
        self.N = 0
        self.zjiaodu = 0
        self.zzhayan = 0
        self.zjuli = 0
        self.jread()
        self.zhayancishu()
        self.jiaodu()
        self.juli()

    def xuanzhuan90(self, x):
        """
        :param x:图片数组
        :return: 旋转90度后的图片数组
        """
        x = np.transpose(x, (1, 0, 2))
        x = x[:, ::-1, :]
        return x

    def jread(self):
        """
        读取视频文件
        :return:
        """
        #        flag=0
        input_movie = cv2.VideoCapture(self.filename)
        length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
        self.data['length'] = length
        self.data['type'] = 'face'
        facial_features = [
            'left_eye',
            'right_eye',
            'top_lip',
            'bottom_lip'
        ]
        frame_number = 0
        self.data['frame'] = []
        for facial_feature in facial_features:
            self.data[facial_feature] = []
        while True:
            ret, frame = input_movie.read()
            if (not ret):
                break
            frame_number += 1

            # print(frame_number)
            #             xxx=find_face(frame,frame_number)
            #             if xxx!=[]:
            #                 self.farr.append(xxx)

            rgb_frame = frame[:, :, ::-1]  # need attention
            count = 0
            face_landmarks_list = face_recognition.face_landmarks(rgb_frame)
            while (count < 3 and len(face_landmarks_list) == 0):
                rgb_frame = self.xuanzhuan90(rgb_frame)
                face_landmarks_list = face_recognition.face_landmarks(rgb_frame)
                count += 1
            self.data['frame'].append(frame_number)
            if len(face_landmarks_list) != 0:
                face_landmarks = face_landmarks_list[0]
                for facial_feature in facial_features:
                    self.data[facial_feature].append(face_landmarks[facial_feature])
            else:
                #                flag=1
                for facial_feature in facial_features:
                    self.data[facial_feature].append([])
        #        print(filename)
        #        print('flag%d'%flag)
        input_movie.release()
        cv2.destroyAllWindows()

        self.N = (len(self.data['left_eye']))
        self.zs = self.N / 15

    def time2zhen(self, x, y):
        """
        将时间转化为图片帧数
        :param x: 下边界
        :param y: 上边界
        :return:
        """
        return math.ceil(self.zs * x), math.floor(self.zs * y)

    def euldist(self, x, y):
        """
        两点之间欧式距离
        :param x:
        :param y:
        :return:
        """
        x = np.array(x)
        y = np.array(y)
        return (np.sqrt(np.sum(np.square(x - y))))

    def eyebili(self, x):
        """
        眼上下点与左右点间距比例
        :param x:
        :return:
        """
        return (self.euldist(x[1], x[5]) + self.euldist(x[2], x[4])) / (2 * self.euldist(x[0], x[3]))

    def blink(self, x):
        """
        眼比例数组
        :param x:
        :return:
        """
        bl = []
        l = len(x)
        for i in range(l):
            if x[i] == []:
                continue
            else:
                bl.append(self.eyebili(x[i]))
        return bl

    def jisuaneyeyuzhi(self, type, bl):
        """
        计算眨眼阈值
        :param type:
        :param bl:
        :return:
        """
        if type == 1:
            return 1 / 4
        else:
            x = np.array(bl)
            return np.mean(x)

    def zhayan(self, x):
        """
        计算眨眼次数
        :param x:
        :return:
        """
        bl = self.blink(x)
        yuzhi = self.jisuaneyeyuzhi(2, bl)
        #     print(bl)
        #     print(yuzhi)
        #     plt.figure()
        #     plt.plot(bl)
        #     plt.show()
        countci = 0
        countfr = []
        l = len(bl)
        i = 0
        while i < l:
            if (bl[i] < yuzhi / 1.4):
                countci += 1
                tempcount = 0
                #             print(i)
                #             print(bl[i])
                while bl[i] < yuzhi / 1.22:
                    #                 if bl[i]<(yuzhi/1.3):
                    tempcount += 1
                    i += 1
                #             print(i)
                #             print(bl[i])
                if tempcount >= self.zs or tempcount < (math.floor(self.zs * 0.2) + 1):
                    countci -= 1
                else:
                    countfr.append(tempcount)
            else:
                i += 1
        if len(countfr) > 0:
            frmean = np.mean(np.array(countfr))
        else:
            frmean = 0
        return [countci, frmean]

    def zhacount(self, x):
        """
        计算时间区间内眨眼次数
        :param x:
        :return:
        """
        xtemp = np.array(x)
        a, b = self.time2zhen(1, 14.4)
        [count, mean] = self.zhayan(x[a:b])
        return (count)

    def zhayancishu(self):
        """
        计算左右眼眨眼次数平均值
        :return:
        """
        a1 = self.zhacount(self.data['left_eye'])
        a2 = self.zhacount(self.data['right_eye'])
        self.zzhayan = math.floor((a1 + a2) / 2)

    def jisuanjiaodu(self, x, y):
        """
        计算嘴角角度
        :param x:
        :param y:
        :return:
        """
        deltax = x[0] - y[0]
        deltay = x[1] - y[1]
        if deltax == 0:
            if x[1] > y[1]:
                return math.pi / 2
            else:
                return -math.pi / 2
        else:
            return math.atan(deltay / deltax)

    def jiaodu(self):
        """
        计算角度数组的平均值
        :return:
        """
        jiaodu1 = []
        x = self.data['top_lip']
        a, b = self.time2zhen(12, 14)
        x = x[a:b]
        l = len(x)
        for i in range(l):
            xtemp = x[i]
            temp = []
            if xtemp == []:
                pass
            else:
                temp.append(self.jisuanjiaodu(xtemp[0], xtemp[1]))
                #             temp.append(jisuanjiaodu(xtemp[1],xtemp[2]))
                #             temp.append(jisuanjiaodu(xtemp[0],xtemp[-1]))
                #             temp.append(jisuanjiaodu(xtemp[-1],xtemp[-2]))
                jiaodu1.append(temp)
        #     stat=[]
        #     jiaodu1=np.array(jiaodu1)
        jiaodu = np.mean(np.array(jiaodu1))
        jiaodu = jiaodu / math.pi * 180
        self.zjiaodu = jiaodu

    def juli(self):
        """
        计算上下嘴唇距离
        :return:
        """
        juli = []
        y1 = self.data['top_lip']
        y2 = self.data['bottom_lip']
        a, b = self.time2zhen(1, 10)
        y1 = y1[a:b]
        y2 = y2[a:b]
        l1 = len(y1)
        l2 = len(y2)
        if l1 < l2:
            l = l1
        else:
            l = l2
        for i in range(l):
            if y1[i] == [] or y2[i] == []:
                pass
            else:
                juli.append(self.euldist(y1[i][9], y2[i][9]))
        juli1 = np.mean(np.array(juli))
        self.zjuli = juli1

    def getjuli(self):
        """
        返回上下嘴距离
        :return:
        """
        return self.zjuli

    def getjiaodu(self):
        """
        返回嘴角角度
        :return:
        """
        return self.zjiaodu

    def getzhayan(self):
        """
        返回眨眼次数
        :return:
        """
        return self.zzhayan

def test():
    """
    测试函数
    :return:
    """
    filename = './data/于金平_Face_2018-07-03_12-02-12_38.mp4'
    fac = face_fea(filename)
    print(fac.getzhayan())
    print(fac.getjiaodu())
    print(fac.getjuli())