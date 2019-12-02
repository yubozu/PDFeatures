import numpy as np
import pandas as pd
import json
from matplotlib import pyplot as plt


class Stride_fea():
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

    def get_pedometer(self):
        """
        计算步数
        :return:
        """
        a, b, c = count_steps(self.data['a'])
        return a

    def get_start_time(self):
        """
        启动反应时间
        :return:
        """
        a, b, c = count_steps(self.data['a'])
        return b

    def get_step_var(self):
        """
        计算步伐间隔方差
        :return:
        """
        a, b, c = count_steps(self.data['a'])
        return c


def count_steps(data):
    threshold = 0.5
    smoothing = 6
    self_weight = 1.5

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
    # plot
    #     plt.plot(data, 'g-', label='input')
    #     plt.plot(smoothed['values'], 'k-', label='smoothed')
    #     plt.plot(smoothed['peaks'], 'ro', label='peaks')
    #     plt.xlabel('sample #')
    #     plt.ylabel('gravitational force [g]')
    #     plt.legend()
    #     plt.show()
    #     print('Number of steps: ', smoothed['peaks'].count())
    via = 0.0
    for t in range(len(stepTime) - 1):
        via = via + ((stepTime[t + 1] - stepTime[t]) ** 2) / float(len(stepTime) - 1)

    return smoothed['peaks'].count(), stepTime[0] / 50.0, via

def test():
    """
    测试函数
    :return:
    """
    file = './data/陈家恒_Stride_2018-07-23_14-59-19_9.txt'
    stride = Stride_fea(file)
    print('步数：',stride.get_pedometer())
    print('启动时间距离测试开始',stride.get_start_time(),'s')
    print('步伐间隔方差:',stride.get_step_var())

#     print(tap.rightcount())
#     print(tap.rightflu())
#     print(tap.allcount())
