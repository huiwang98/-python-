# coding=utf-8
# myApriori.py
# from numpy import *
# import pandas as pd
import time

def getC1(transactions):
    C1 = []
    for itemSet in transactions:
        for item in itemSet:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return C1


def getSubListByIndex(input, index):
    output=[]
    for i in index:
        output.append(input[i])
    return output


def getSubListByMin(input, min):
    output=[]
    index=[]
    for i in range(len(input)):
        if input[i] >= min:
            output.append(input[i])
            index.append(i)
    return output, index


def getL(C, S, minSup):
    sup, index=getSubListByMin(S, minSup)
    L = getSubListByIndex(C, index)
    return L, sup


def genNextC(C):
    nextC=[]
    lenOfTran = len(C)
    lenOfItemSet = len(C[0])
    for i in range(lenOfTran):
        for j in range(i+1,lenOfTran):
            newItemSet=list(set(C[i]).union(set(C[j])))
            testSet=list(set(C[i][:-1]).union(set(C[j][:-1])))
            if len(newItemSet) == lenOfItemSet+1 and len(testSet) == lenOfItemSet-1 :
                t = list(newItemSet)
                t.sort()
                nextC.append(t)
    return nextC


def getSup(data, C):
    sup=[]
    for i in C:
        count = 0
        for j in data:
            if set(i).issubset(set(j)):
                count += 1
        sup.append(count)
    return sup


def genRules(traceL, traceS, minConf):
    for i in range(1,len(traceL)):
        for j in range(len(traceL[i])):
            freqSet = traceL[i][j]
            sup = traceS[i][j]
            findRule(freqSet, sup, traceL, traceS, minConf)


def findRule(freqSet, sup, traceL, traceS, minConf):
    for i in range(len(freqSet)-1):
        for j in range(len(traceL[i])):
            t_con = sup/traceS[i][j]
            if set(traceL[i][j]).issubset(set(freqSet)) and t_con >= minConf:
                t_A = traceL[i][j]
                t_B = list(set(freqSet)-set(traceL[i][j]))
                print("{0}-->{1},置信度{2}".format(t_A, t_B, t_con))


t1 = time.time()
dataFile = 'apriori_task.txt' # 输入事务集文件
minSupport = 0.06
minConf = 0.75
file = open(dataFile)
data = file.read()
dataT = data.split("\n")
data = []
for i in dataT:
    data.append(i.split(","))
lenOfData=len(data)
minSup = minSupport * lenOfData
traceL = []
traceS = []
C1 = getC1(data)
S1 = getSup(data, C1)
L1, S1 = getL(C1, S1, minSup)
traceL.append(L1)
traceS.append(S1)
Lk = L1
while len(Lk) != 0:
    Ck = genNextC(Lk)
    Sk = getSup(data, Ck)
    Lk, Sk = getL(Ck, Sk, minSup)
    traceL.append(Lk)
    traceS.append(Sk)
for i in range(len(traceL)):
    for j in range(len(traceL[i])):
        print("{0}的支持度为{1}".format( traceL[i][j],traceS[i][j]/lenOfData))
print("-"*40)
genRules(traceL, traceS, minConf)
t2 = time.time()
print("时间：",t2-t1)
