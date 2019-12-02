import numpy as np
import pandas as pd
import json

# from scipy.fftpack import fft,ifft
from matplotlib import pyplot as plt
from matplotlib.pylab import mpl


class Tremor_fea():
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
        return self.data['a']

    def get_avg(self):
        """
        统计震颤平均幅度
        :return:
        """
        return np.array(self.data['a']).mean()

    def get_freq(self):
        """
        计算震颤频率
        :return:
        """
        #         a = smooth(self.data['a'])
        #         b = smooth(a['values'])
        x = self.data['a'] - np.array(self.data['a']).mean()
        #         plt.plot(x)
        fft_y = np.fft.fft(x)
        #         print(len(fft_y))
        #         print(fft_y)
        abs_y = np.abs(fft_y)
        abs_y_half = abs_y[:int(len(abs_y) / 2)]
        #         plt.figure()
        #         plt.plot(np.arange(int(len(abs_y_half))),abs_y_half)
        f_0_175, f_175_350, f_350_650, f_650_850, f_850_2500 = 0, 0, 0, 0, 0
        for i in range(int(len(abs_y_half))):
            if i < (1.75 / 25 * int(len(abs_y_half))):
                f_0_175 += abs_y_half[i] ** 2
            elif i < (3.5 / 25 * int(len(abs_y_half))):
                f_175_350 += abs_y_half[i] ** 2
            elif i < (6.5 / 25 * int(len(abs_y_half))):
                f_350_650 += abs_y_half[i] ** 2
            elif i < (8.5 / 25 * int(len(abs_y_half))):
                f_650_850 += abs_y_half[i] ** 2
            else:
                f_850_2500 += abs_y_half[i] ** 2

        #         print(f_0_175)
        #         print(f_175_350)
        #         print(f_350_650)
        #         print(f_650_850)
        #         print(f_850_2500)
        maxfreq = 0
        freq = ''
        for i in ['f_0_175', 'f_175_350', 'f_350_650', 'f_650_850', 'f_850_2500']:
            if eval(i) > maxfreq:
                freq = i

        return freq

    def get_freq_rate(self):
        """
        计算震颤大于阈值时间比
        :return:
        """
        rate = 0.0
        x = self.data['a'] - np.array(self.data['a']).mean()
        for i in range(len(x)):
            if x[i] > 0.5:
                rate += 1
        return rate / len(x)

# 绘制 0 1 2 3 患者震颤图像：0.5作为区分即可

# file = ['./data/黄长瑞_Tremor_LR_2018-01-16_15-43-45_17.txt','./data/姚今观_Tremor_LR_2018-07-16_10-59-17_165.txt','./data/凌玲_Tremor_LR_2018-01-17_09-20-42_16.txt','./data/张宝林_Tremor_LR_2018-02-08_09-09-21_21.txt']

# tremor0 = Tremor_fea(file[0]).readfile()
# tremor1 = Tremor_fea(file[1]).readfile()
# tremor2 = Tremor_fea(file[2]).readfile()
# tremor3 = Tremor_fea(file[3]).readfile()
# plt.subplot(411)
# plt.plot(tremor0 - np.array(tremor0).mean())
# plt.subplot(412)
# plt.plot(tremor1 - np.array(tremor1).mean())
# plt.subplot(413)
# plt.plot(tremor2 - np.array(tremor2).mean())
# plt.subplot(414)
# plt.plot(tremor3 - np.array(tremor3).mean())


def test():
    """
    测试函数
    :return:
    """
    file = './data/罗秋红_Tremor_LR_2018-12-31_16-24-46_3.txt'
    tremor = Tremor_fea(file)
    print('平均幅度：', tremor.get_avg())
    print('震颤频率：', tremor.get_freq(), 'Hz')
    print('震颤大于阈值时间比:', tremor.get_freq_rate())

