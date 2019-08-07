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


NumOfCluster = 3
pointSet = readDataFile("聚类数据样本.csv")
pointSet = np.array(pointSet)
distances = creatDistanceArray(pointSet)
for i in range(len(distances)):
    distances[i,i] = float("inf")  # 把对角线设为正无穷
C = []
for i in range(len(pointSet)):
    C.append([i])
trace = []
while len(C) > NumOfCluster:
    minDist = float("inf")
    IJ = (-1, -1)
    for i in range(0, len(distances)-1):
        for j in range(i+1, len(distances)):
            if distances[i, j] < minDist:
                minDist = distances[i, j]
                IJ = (i, j)
    C[IJ[0]] = C[IJ[0]] + C[IJ[1]]
    del C[IJ[1]]
    for i in range(len(distances)):  # 更新距离表
        distances[IJ[0], i] = min(distances[IJ[0], i], distances[IJ[1], i])  # 最短距离作为簇距离
        distances[i, IJ[0]] = min(distances[i, IJ[0]], distances[i, IJ[1]])
    distances = np.delete(distances, IJ[1], axis=0)
    distances = np.delete(distances, IJ[1], axis=1)
    trace.append(IJ)
pass
# 可视化
clusterNo = [0]
clusterNo = clusterNo * len(pointSet)
for i, cluster in enumerate(C):
    for j in cluster:
        clusterNo[j] = i + 1
tsne = TSNE()
pointSet_2d = tsne.fit_transform(pointSet)  # 进行数据降维,降成两维
pattern = ['k*', 'r.', 'go', 'b*', 'y.', 'mo']
for i in range(len(pointSet_2d)):
    plt.plot(pointSet_2d[i, 0], pointSet_2d[i, 1], pattern[clusterNo[i] % len(pattern)])
plt.show()
