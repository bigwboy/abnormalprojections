# -*- coding: utf8 -*-
#time:2017/8/20 下午5:31
#VERSION:1.0
#__OUTHOR__:guangguang
from datetime import datetime

import xlrd,re

def OpenFile(FILENAME):
    WorkBook=xlrd.open_workbook(FILENAME)
    BookSheet=WorkBook.sheet_by_name('Sheet1')
    WorkDate={}
    WeekDate={}
    FileDate=[]
    for nrow in range(1,BookSheet.nrows):
        try:
            time=BookSheet.cell(nrow,0)
            time=xlrd.xldate.xldate_as_datetime(time.value, 0)
            Key = time.strftime("%Y-%m-%d")
            Value = BookSheet.cell(nrow, 1)
            day_now=datetime.today()
            q=day_now.date()-time.date()
            if (day_now.date()-time.date()).days<30:
                if time.weekday()<5: #平时数据
                    WorkDate[Key]=Value.value
                else: #周末数据
                    WeekDate[Key]=Value.value

        except Exception,e:
            #print '读取文件错误'+str(e)
            pass
    FileDate.append(WorkDate)
    FileDate.append(WeekDate)
    return FileDate

import numpy


class CalculationsEngine():
    #FlowDictoonary={key:日期
    #                value:流量值 }
    def __init__(self,FlowDictoonary,AmountOfUsers):
        self.AmountOfUsers=AmountOfUsers
        self.UnitFlowDictoonary={}
        for key in FlowDictoonary:
            try:
                self.UnitFlowDictoonary[key] = (FlowDictoonary[key] / self.AmountOfUsers)
            except Exception,e:
                #print '数据类型错误:'+str(e)
                #print str(key)
                pass
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
        print "流量最大预警值： " + str(self.UpInsideFance * self.AmountOfUsers)
        print "流量最小预警值： " + str(self.DownInsideFance * self.AmountOfUsers)
        print "流量最大异常值： " + str(self.UpOutsideFance * self.AmountOfUsers)
        print '流量最小异常值:  ' + str(self.DownOutsideFance * self.AmountOfUsers)

        for key  in self.UnitFlowDictoonary:
            #z得分
            Z= (self.UnitFlowDictoonary[key]-self.Mean)/self.StandardDeviation
            if abs(Z)<2:
                print '流量正常 '+key + '\t' + str(self.UnitFlowDictoonary[key]*self.AmountOfUsers)
            elif abs(Z)>3:
                if Z>0:
                    print '流量异常：流量最大异常值 '+key +'\t'+str(self.UnitFlowDictoonary[key]*self.AmountOfUsers)
                else:
                    print '流量异常：流量最小异常值 '+ key +'\t'+str(self.UnitFlowDictoonary[key]*self.AmountOfUsers)
            else:
                if Z>0:
                    print '流量告警：流量最大预警值 '+key + '\t' + str(self.UnitFlowDictoonary[key]*self.AmountOfUsers)
                    print
                else:
                    print '流量告警：流量最小预警值'+key + '\t' + str(self.UnitFlowDictoonary[key]*self.AmountOfUsers)


if __name__=="__main__":
    Date = OpenFile(u'外地统计.xlsx')
    print '平时数据：'
    Check=CalculationsEngine(Date[0],100)
    Check.ReturnData()
    print '周末数据：'
    Check = CalculationsEngine(Date[1], 100)
    Check.ReturnData()
