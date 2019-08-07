# coding=utf-8
# myFP.py
import time
class FPtreeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.nameValue = nameValue
        self.numOccur = numOccur
        self.parentNode = parentNode
        self.sonNode = []


def countSameTransaction(data):
    dataGrouped = {}
    for i in data:
        if frozenset(i) in dataGrouped.keys():  # 这样每次都要将字典key组装成列表，字典可以直接 if key_obj in dict
            dataGrouped[frozenset(i)] = dataGrouped[frozenset(i)]+1
        else:
            dataGrouped[frozenset(i)] = 1  #为什么这里用list不行，用frozenset就可以？因为key值必须是不可修改类型。
    return dataGrouped


def buildHeader(dataGrouped,minSupN):
    headerTable = {}
    for i in dataGrouped:
        for j in i:
            if j in headerTable.keys():
                headerTable[j] = [headerTable[j][0]+dataGrouped[i],[]]
            else:
                headerTable[j] = [dataGrouped[i],[]]
    # keys = list(headerTable.keys())
    keys = headerTable.copy().keys()
    # 不加这两句之一的话，就会出现迭代过程中字典大小改变的错误
    # 猜是因为list是值传递，headerTable.keys()是引用传递
    for i in keys:
        if headerTable[i][0] < minSupN:
            del(headerTable[i])
    headerTable = dict(sorted(headerTable.items(),key=(lambda x:x[1]),reverse=True))  # 排序
    return headerTable


def buildFPTree(headerTable, dataGrouped):
    FPTreeRoot=FPtreeNode("Null", 1, [])
    keys = dataGrouped.keys()
    for i in keys:
        transaction = list(i)
        if len(transaction) > 0:
            num = dataGrouped[i]
            updateNode(FPTreeRoot, transaction, num, headerTable)
    return FPTreeRoot


def updateNode(nodeUpdated, tansaction, num, headerTable):
    t_tansaction=[]
    for t_item in headerTable.keys():
        if t_item in tansaction:
            t_tansaction.append(t_item)
    tansaction=t_tansaction
    if(len(tansaction) == 0):
        return 0
    sonNodes = nodeUpdated.sonNode
    sonNodeThis = FPtreeNode(tansaction[0], 0, nodeUpdated)
    for i in sonNodes:# 查找与没有这个儿子
        if i.nameValue == tansaction[0]:
            sonNodeThis = i
            break
    else:# 循环顺利完毕意味没找到这个儿子，奖励执行添加新儿子，并更新头表
        sonNodes.append(sonNodeThis)
        headerTable[sonNodeThis.nameValue][1].append(sonNodeThis)
    sonNodeThis.numOccur += num
    if len(tansaction[1:]) > 0:
        updateNode(sonNodeThis, tansaction[1:], num, headerTable)
    return 1


def findFreq(headerTable, minSupN, freqDict, endWith ):
    for i in list(headerTable.keys())[::-1]:
        thisItem = i
        thisEndWith = [i] + endWith
        if headerTable[thisItem][0] >= minSupN:
            freqDict[frozenset(thisEndWith)] = headerTable[thisItem][0]
        paths = {} # 生成条件模式基 dict
        for j in headerTable[thisItem][1]:
            path = findPath(j)
            paths[frozenset(path)] = j.numOccur
        newHeaderTable = buildHeader(paths, minSupN)
        buildFPTree(newHeaderTable, paths)
        if len(newHeaderTable) > 0:
            freqDict = findFreq(newHeaderTable, minSupN, freqDict, thisEndWith)
    return freqDict


def findPath(node): #返回list
    t_node = node.parentNode
    path = []
    while t_node.nameValue != "Null":
        path.insert(0, t_node.nameValue)
        t_node = t_node.parentNode
    return path


def dict2list(freqDict):
    maxLength = 0
    for i in freqDict.keys():
        length = len(list(i))
        maxLength = max(length, maxLength)
    # traceL = [[] * maxLength]
    # traceS = [[] * maxLength] # 错的
    traceL = []
    traceS = []
    for i in range(maxLength):
        traceL.append([])
        traceS.append([])
    for i in freqDict.keys():
        length = len(list(i))
        traceL[length - 1].append(list(i))
        traceS[length - 1].append(freqDict[i])
    return traceL, traceS


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
dataFile = "apriori_task.txt" # 输入事务集文件
file = open(dataFile)
data = file.read()
dataT = data.split("\n")
data = []
for i in dataT:
    data.append(i.split(","))
lenOfData = len(data)
minSupport = 0.06
minConf = 0.75
minSupN = minSupport * lenOfData
dataGrouped = countSameTransaction(data)
headerTable = buildHeader(dataGrouped, minSupN)
FPTree = buildFPTree(headerTable, dataGrouped)
freqDict = {}
endWith = []
freqDict = findFreq(headerTable, minSupN, freqDict, endWith)
traceL, traceS = dict2list(freqDict)
genRules(traceL, traceS, minConf)
t2 = time.time()
print("时间：",t2-t1)
