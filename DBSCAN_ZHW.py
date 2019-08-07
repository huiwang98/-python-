import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def readDataFile(dataFile):
    data = open(dataFile, 'r', encoding='utf-8-sig')
    dataSet = data.read()
    dataSet = dataSet.split("\n")
    for i in range(len(dataSet)):
        dataSet[i] = dataSet[i].split(",")
    dataSet = [[float(x) for x in row] for row in dataSet]
    return dataSet


def creatDistanceArray(pointSet):
    dataSize = len(pointSet)
    distances = np.zeros((dataSize, dataSize))
    for i in range(dataSize):
        for j in range(i, dataSize):
            d = np.linalg.norm(pointSet[i, ] - pointSet[j, ])  # 二范数 欧氏距离
            distances[i, j] = d
            distances[j, i] = d
    return distances


def getNeighbor(distances, index, r):
    N = list()
    for i, distance in enumerate(distances[index]):
        if distance <= r:
            N.append(i)
    return N


minPts = 5
r = 0
pointSet = readDataFile("聚类数据样本.csv")
pointSet = np.array(pointSet)
pointSet = np.hstack((pointSet, np.ones((len(pointSet), 1))*(-1) ))
distances = creatDistanceArray(pointSet)
r = np.percentile(distances, 10, interpolation='midpoint')
for i, point in enumerate(pointSet):
    if point[-1] == -1:  # 未聚类
        N = getNeighbor(distances, i, r)
        if len(N) >= minPts:  # 是核心
            thisClusterNo = max(pointSet[:, -1].max() + 1, 1)  # 给予编号
            pointSet[i, -1] = thisClusterNo
            while len(N) > 0:
                n = N.pop()
                if pointSet[n, -1] != -1:
                    continue
                t = getNeighbor(distances, n, r)
                if len(t) >= minPts:  # 邻居是核心
                    N = N + t
                pointSet[n, -1] = thisClusterNo
        else:  # 非核心
            pointSet[i, -1] = 0
print("总聚类数：", pointSet[:, -1].max())
print("离群点数：", len(pointSet[(pointSet[:, -1] == 0), :]))
# 可视化
tsne = TSNE()
pointSet_2d = tsne.fit_transform(pointSet[:, 0:-1])  # 进行数据降维,降成两维
pattern = ['k*', 'r.', 'go', 'b*', 'y.', 'mo']
for i in range(len(pointSet_2d)):
    plt.plot(pointSet_2d[i, 0], pointSet_2d[i, 1], pattern[int(pointSet[i, -1]) % len(pattern)])
plt.show()
