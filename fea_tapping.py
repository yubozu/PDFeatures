#coding=utf-8
import numpy as np
import json


class tapping_fea():

    def __init__(self, filename):
        """
        :param filename:需要处理的文件
        """
        self.filename = filename
        self.data = {}
        self.jread()

    def jread(self):
        """
        读入文件
        :return:
        """
        f = open(self.filename)
        s = f.readline()
        js = json.loads(s)
        type = js['type']
        if type.find('fir') >= 0:
            type = 'Tapping_R'
            sss = 'finger'
        else:
            if type.find('fil') >= 0:
                type = 'Tapping_L'
                sss = 'finger'
            else:
                sss = 'btn'
        data1 = js['data']
        jdata = data1
        btn = []
        timeTemp = []
        for item in jdata:
            time_stamp = (item['time'])
            x = item[sss]
            btn.append(x)
            timeTemp.append(time_stamp)
        l = len(timeTemp)
        self.data['type'] = type
        self.data['datapoision'] = False

        timeTempt = []
        btnt = []
        for i in range(l):
            if (timeTemp[i] - timeTemp[0] > 999 and timeTemp[i] - timeTemp[0] < 14001):
                timeTempt.append(timeTemp[i])
                btnt.append(btn[i])
        self.data['time'] = timeTempt
        self.data['btn'] = btnt

    def rightcount(self):
        """
        计算正确敲击次数
        :return:
        """
        tapHand = np.array(self.data['btn'])
        if len(tapHand) == 0:
            return 0
        count = 1
        for i in range(1, len(tapHand)):
            if tapHand[i] != tapHand[i - 1]:
                count += 1
        return count

    def rightflu(self):
        """
        计算正确敲击时间间隔波动
        :return:
        """
        tapHand = np.array(self.data['btn'])
        if len(tapHand) < 2:
            return 10000000
        crossTime = []
        time = np.array(self.data['time'])
        last1 = time[0]
        cT = []
        allT = []
        for i in range(1, len(tapHand)):
            allT.append(time[i] - time[i - 1])
            if tapHand[i] == tapHand[i - 1]:
                continue
            else:
                crossTime.append(time[i] - time[i - 1])
                cT.append(time[i] - last1)
                last1 = time[i]
        ctb = np.mean(cT)
        flu = np.mean(np.abs(cT - ctb))
        return flu

    def allcount(self):
        """
        返回总次数
        :return:
        """
        return (len(self.data['btn']))

def test():
    """
    测试函数
    :return:
    """
    file = './data/何云喜_Tapping_L_2018-07-05_15-18-43_51.txt'
    tap = tapping_fea(file)
    print(tap.rightcount())
    print(tap.rightflu())
    print(tap.allcount())