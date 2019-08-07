from math import log


def calcShannonEnt(dataSet):  # 计算信息熵
    numEntries = len(dataSet)
    labelCounts = {}
    # 给所有可能分类创建字典
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    # 以2为底数计算香农熵
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


def classifyOnce(dataset):
    classifierTree = {}
    sethannonEnt = calcShannonEnt(dataset)
    if sethannonEnt == 0:
        return {dataset[0][-1]}
    else:
        attrIndex, datasetDivided = findBestDivi(dataset)
        for i in datasetDivided.keys():
            classifierTree[i] = classifyOnce(datasetDivided[i])
    return classifierTree


def findBestDivi(dateset):
    datasetBestDivided = {}
    maxGain = -10000
    attrIndex = -1
    info = calcShannonEnt(dateset)
    for i in range(len(dataset[0])-1):
        datasetDivided = divideDataset(i, dateset)
        if len(datasetDivided) <= 1:  # 如果当前划分没有划分性，跳过（挖坑：并没有处理所有属性都没有划分性，但label却不一致的情况）
            continue
        currentGain = calcGain(datasetDivided,info)
        if currentGain>maxGain:
            maxGain = currentGain
            datasetBestDivided = datasetDivided
            attrIndex = i
    return attrIndex, datasetBestDivided


def divideDataset(index, dataset) :
    datasetDivided = {}
    for i in dataset:
        if i[index] not in datasetDivided.keys():
            datasetDivided[i[index]] = []
        datasetDivided[i[index]].append(i)

    return datasetDivided


def calcGain(datasetDivided, info) :
    infoA = 0
    totalNum = 0
    for i in datasetDivided.keys():
        totalNum += len(datasetDivided[i])
    for i in datasetDivided.keys():
        infoA += calcShannonEnt(datasetDivided[i]) * len(datasetDivided[i]) / totalNum
    gain = info - infoA
    return gain

### main
wmdata3_o = [
    [1, "青绿", "蜷缩", "浊响", "清晰", "凹陷", "硬滑", 0.697, 0.46, 1],
    [2, "乌黑", "蜷缩", "沉闷", "清晰", "凹陷", "硬滑", 0.774, 0.376, 1],
    [3, "乌黑", "蜷缩", "浊响", "清晰", "凹陷", "硬滑", 0.634, 0.264, 1],
    [4, "青绿", "蜷缩", "沉闷", "清晰", "凹陷", "硬滑", 0.608, 0.318, 1],
    [5, "浅白", "蜷缩", "浊响", "清晰", "凹陷", "硬滑", 0.556, 0.215, 1],
    [6, "青绿", "稍蜷", "浊响", "清晰", "稍凹", "软粘", 0.403, 0.237, 1],
    [7, "乌黑", "稍蜷", "浊响", "稍糊", "稍凹", "软粘", 0.481, 0.149, 1],
    [8, "乌黑", "稍蜷", "浊响", "清晰", "稍凹", "硬滑", 0.437, 0.211, 1],
    [9, "乌黑", "稍蜷", "沉闷", "稍糊", "稍凹", "硬滑", 0.666, 0.091, 0],
    [10, "青绿", "硬挺", "清脆", "清晰", "平坦", "软粘", 0.243, 0.267, 0],
    [11, "浅白", "硬挺", "清脆", "模糊", "平坦", "硬滑", 0.245, 0.057, 0],
    [12, "浅白", "蜷缩", "浊响", "模糊", "平坦", "软粘", 0.343, 0.099, 0],
    [13, "青绿", "稍蜷", "浊响", "稍糊", "凹陷", "硬滑", 0.639, 0.161, 0],
    [14, "浅白", "稍蜷", "沉闷", "稍糊", "凹陷", "硬滑", 0.657, 0.198, 0],
    [15, "乌黑", "稍蜷", "浊响", "清晰", "稍凹", "软粘", 0.36, 0.37, 0],
    [16, "浅白", "蜷缩", "浊响", "模糊", "平坦", "硬滑", 0.593, 0.042, 0],
    [17, "青绿", "蜷缩", "沉闷", "稍糊", "稍凹", "硬滑", 0.719, 0.103, 0]
]
dataset = [i[1:-3] for i in wmdata3_o] # 取数据中的需要部分
for i in range(len(wmdata3_o)):
    dataset[i].append(wmdata3_o[i][-1])
t=calcShannonEnt(dataset)
classifierTree = classifyOnce(dataset)
print(classifierTree)
