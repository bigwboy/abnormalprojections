# -*- coding: utf8 -*-
#time:2017/8/20 下午5:31
#VERSION:1.0
#__OUTHOR__:guangguang

import xlrd

def OpenFile(FILENAME):
    pass




import numpy


class CalculationsEngine():
    #FlowDictoonary={key:日期
    #                value:流量值 }
    def __init__(self,FlowDictoonary,AmountOfUsers):
        self.FlowDictoonary=FlowDictoonary
        self.AmountOfUsers=AmountOfUsers
        self.UnitFlowDictoonary={}
        pass
    def GetData(self):
        pass
    def CalculationsUnitFlow(self): #计算单位用户流量并进行排序（升序）
        for key in self.FlowDictoonary:
            self.UnitFlowDictoonary[key]=(self.FlowDictoonary[key]/self.AmountOfUsers)
        return self.UnitFlowDictoonary
    def Calculation(self):#离散计算
        #均值
        self.Mean=numpy.mean(self.UnitFlowDictoonary.values())
        #上4分位
        self.Up4Score=numpy.percentile(self.UnitFlowDictoonary.values(),75)
        #下4分位
        self.Down4Score=numpy.percentile(self.UnitFlowDictoonary.values(),25)
        #标准差
        self.StandardDeviation=numpy.std(self.UnitFlowDictoonary.values())
        #4分位差
        self.IRQ=self.Up4Score-self.Down4Score
        #上内篱笆
        self.UpInsideFance=self.Up4Score+1.5*self.IRQ
        #下内篱笆
        self.DownInsideFance=self.Down4Score-1.5*self.IRQ
        #上外篱笆
        self.UpOutsideFance=self.Up4Score+3*self.IRQ
        #下外篱笆
        self.DownOutsideFance=self.Down4Score-3*self.IRQ
        pass
    def ReturnData(self):
        for key  in self.UnitFlowDictoonary:
            #z得分
            Z= (self.UnitFlowDictoonary[key]-self.Mean)/self.StandardDeviation
            if abs(Z)<2:
                break
            elif abs(Z)>3:
                if Z>0:
                    print '流量异常：高于上外篱笆值'
                    print key +'\:'+self.UnitFlowDictoonary[key]
                else:
                    print '流量异常：低于下外篱笆值'
                    print key +'\:'+self.UnitFlowDictoonary[key]
            else:
                if Z>0:
                    print '流量告警：高于上内篱笆值'
                    print key + '\:' + self.UnitFlowDictoonary[key]
                else:
                    print '流量告警：低于下内篱笆值'
                    print key + '\:' + self.UnitFlowDictoonary[key]


if __name__=="__main__":
    pass