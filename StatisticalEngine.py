# -*- coding: utf8 -*-
#time:2017/8/20 下午5:31
#VERSION:1.0
#__OUTHOR__:guangguang
from datetime import datetime

import xlrd,re

def OpenFile(FILENAME):
    WorkBook=xlrd.open_workbook(FILENAME)
    BookSheet=WorkBook.sheet_by_name('Sheet1')
    p={}
    FileDate={}
    for nrow in range(1,BookSheet.nrows):
        try:
            time=BookSheet.cell(nrow,0)
            time=xlrd.xldate.xldate_as_datetime(time.value, 0)
            if time.weekday()<5: #平时数据
                Key=time.strftime("%Y-%m-%d")
                Value=BookSheet.cell(nrow,1)
                FileDate[Key]=Value.value
            else: #周末数据
                pass
        except Exception,e:
            print '读取文件错误'+str(e)
    return FileDate

import numpy


class CalculationsEngine():
    #FlowDictoonary={key:日期
    #                value:流量值 }
    def __init__(self,FlowDictoonary,AmountOfUsers):
        self.AmountOfUsers=AmountOfUsers
        self.UnitFlowDictoonary={}
        for key in FlowDictoonary:
            self.UnitFlowDictoonary[key] = (FlowDictoonary[key] / self.AmountOfUsers)
    def GetData(self):
        pass
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

    def ReturnData(self):
        self.Calculation()
        print "均值： " + str(self.Mean * self.AmountOfUsers)
        print "标准差： " + str(self.StandardDeviation * self.AmountOfUsers)
        print "上内篱笆： " + str(self.UpInsideFance * self.AmountOfUsers)
        print "下内篱笆： " + str(self.DownInsideFance * self.AmountOfUsers)
        print "上外篱笆： " + str(self.UpOutsideFance * self.AmountOfUsers)
        print '下外篱笆:  ' + str(self.DownOutsideFance * self.AmountOfUsers)

        for key  in self.UnitFlowDictoonary:
            #z得分
            Z= (self.UnitFlowDictoonary[key]-self.Mean)/self.StandardDeviation
            if abs(Z)<2:
                print '流量正常 '+key + '\t' + str(self.UnitFlowDictoonary[key]*self.AmountOfUsers)
            elif abs(Z)>3:
                if Z>0:
                    print '流量异常：高于上外篱笆值 '+key +'\t'+str(self.UnitFlowDictoonary[key]*self.AmountOfUsers)
                else:
                    print '流量异常：低于下外篱笆值 '+ key +'\t'+str(self.UnitFlowDictoonary[key]*self.AmountOfUsers)
            else:
                if Z>0:
                    print '流量告警：高于上内篱笆值 '+key + '\t' + str(self.UnitFlowDictoonary[key]*self.AmountOfUsers)
                    print
                else:
                    print '流量告警：低于下内篱笆值 '+key + '\t' + str(self.UnitFlowDictoonary[key]*self.AmountOfUsers)


if __name__=="__main__":
    Date = OpenFile(u'数据.xlsx')
    Check=CalculationsEngine(Date,100)
    Check.ReturnData()