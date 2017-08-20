# -*- coding: utf8 -*-
#time:2017/8/20 下午5:31
#VERSION:1.0
#__OUTHOR__:guangguang
class CalculationsEngine():
    def __init__(self,FlowDictoonary,AmountOfUsers):
        self.FlowList=FlowDictoonary
        self.AmountOfUsers=AmountOfUsers
        self.UnitFlowList=[]
        pass
    def GetData(self):
        pass
    def CalculationsUnitFlow(self): #计算单位用户流量并进行排序
        for Flow in self.FlowList:
            self.UnitFlowList.append(Flow/self.AmountOfUsers)
        self.UnitFlowList.sort()
    def Calculation(self):
        pass
    def ReturnData(self):
        pass


if __name__=="__main__":
    pass