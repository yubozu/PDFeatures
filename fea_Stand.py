import numpy as np
import pandas as pd
import json
from matplotlib import pyplot as plt


class Stand_fea():
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        self.readfile()

    def readfile(self):
        f = open(self.filename)
        s = f.readline()
        js = json.loads(s)
        data_temp = js['data']
        acc = data_temp['acc']
        self.data['t'] = []
        self.data['a'] = []
        self.data['x'] = []
        self.data['y'] = []
        self.data['z'] = []
        #         t = []
        #         a = []
        #         x = []
        #         y = []
        #         z = []
        #         for item in acc:
        #             for para in ['t','a','x','y','z']:
        #                 eval(para).append(item[para])
        for item in acc:
            for para in ['t', 'a', 'x', 'y', 'z']:
                self.data[para].append(item[para])
        self.data['type'] = js['type']

    #         print(len(self.data['t']))

    def get_jitter(self):
        """
        抖动次数
        :return:
        """
        a = smooth(self.data['a'])
        return a['peaks'].count()

    def get_shaking(self):
        """
        晃动程度
        :return:
        """

        return np.var(self.data['a'])

    def get_avg_shaking(self):
        """
        平均晃动程度
        :return:
        """
        return np.mean(self.data['a'])


def smooth(data):
    threshold = 0.1
    smoothing = 6
    self_weight = 2

    weight = self_weight - 1

    # smoothing
    smoothed = pd.DataFrame(columns=['values', 'peaks'])
    for i in range(len(data)):
        try:
            value = (np.sum(data[i - smoothing: i + smoothing + 1]) + data[i] * weight) / (2 * smoothing + weight + 1)
            # mean of self_weight x self and 2 x smoothing neighbors
            smoothed = smoothed.append({'values': value}, ignore_index=True)
        except KeyError:
            smoothed = smoothed.append({'values': None},
                                       ignore_index=True)  # when there are not enough neighbors on one of the sides
    # peak finding
    mean = smoothed['values'].mean()
    up = mean + threshold  # upper bound
    stepTime = []
    for i, v in enumerate(smoothed['values']):
        try:
            # check if greater than left and right neaighbor and far enough from mean
            if smoothed['values'][i - 1] < v and smoothed['values'][i + 1] < v and v > up:
                smoothed['peaks'][i] = v
                stepTime.append(i)
            else:
                smoothed['peaks'][i] = None
        except KeyError:
            smoothed['peaks'][i] = None

    return smoothed


def test():
    """
    测试函数
    :return:
    """
    file = './data/于海霞_Stand_L_2018-01-24_09-50-10_1.txt'
    stand = Stand_fea(file)
    print('抖动次数：', stand.get_jitter())
    print('晃动程度（方差）：', stand.get_shaking())
    print('平均晃动程度（均值）:', stand.get_avg_shaking())

