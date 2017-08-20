# -*- coding: utf8 -*-
#time:2017/8/20 下午5:31
#VERSION:1.0
#__OUTHOR__:guangguang
class CalculationsEngine():
    #FlowDictoonary={key:日期
    #                value:流量值 }
    def __init__(self,FlowDictoonary,AmountOfUsers):
        self.FlowDictoonary=FlowDictoonary
        self.AmountOfUsers=AmountOfUsers
        self.UnitFlowList={}
        pass
    def GetData(self):
        pass
    def CalculationsUnitFlow(self): #计算单位用户流量并进行排序（升序）
        for key in self.FlowDictoonary:
            self.UnitFlowList[key]=(self.FlowDictoonary[key]/self.AmountOfUsers)
        sorted(self.UnitFlowList.items(),key=lambda asd:asd[0],reverse=False)
    def Calculation(self):
        pass
    def ReturnData(self):
        pass


if __name__=="__main__":
    pass