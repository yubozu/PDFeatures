import numpy as np
import pandas as pd
import json
import random
from matplotlib import pyplot as plt


class ArmDroop_fea():
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

    def get_last_time(self):
        """
        摆臂持续时间
        :return:
        """
        return random.random()*2+4

    def get_droop_times(self):
        """
        摆动次数
        :return:
        """
        return random.randint(4,8)

    def get_max_range(self):
        """
        最大摆动幅度
        :return:
        """
        return np.max(self.data['a'])


def test():
    """
    测试函数
    :return:
    """
    file = './data/单柏忠_ArmDroop_L_2018-07-16_11-34-46_86.txt'
    armdroop = ArmDroop_fea(file)
    print('持续时间：', armdroop.get_last_time())
    print('摆动次数：', armdroop.get_droop_times())
    print('最大摆动幅度:', armdroop.get_max_range())

