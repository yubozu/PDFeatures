#coding=utf-8
import random

class fea_sound():
    def __init__(self,filename):
        self.filename=filename
        self.jitter=random.random()*10
        self.shimmer=random.random()*10
        self.HNR=random.random()*100

    def getjitter(self):
        return self.jitter

    def getshimmer(self):
        return self.shimmer

    def getHNR(self):
        return self.HNR


def test(fileneam):
    s=fea_sound(fileneam)
    print(s.getjitter())
    print(s.getshimmer())
    print(s.getHNR())