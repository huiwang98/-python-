import random
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


def initCluster(pointSet, numOfClu):
    n = len(pointSet)
    randomList = random.sample(range(n), numOfClu)
    centers = []
    for i in randomList:
        centers.append(pointSet[i])
    cluster = getCluster(pointSet, centers)
    return cluster, centers


def isStatic(c1, c2):
    n = len(c1)
    m = len(c1[0])
    for i in range(n):
        for j in range(m):
            if c1[i][j] != c2[i][j]:
                return False
    else:
        return True
    pass


def getCluster(pointSet, centers):
    n = len(centers)
    cluster = []
    for i in range(n):
        cluster.append([])
    for point in pointSet:
        d = []
        for center in centers:
            d.append(distance(point, center))
        cluster[indexOfMin(d)].append(point)
    return cluster


def indexOfMin(arr):
    minindex = 0
    min = arr[0]
    for i in range(len(arr)):
        if arr[i] < min:
            min = arr[i]
            minindex = i
    return minindex


def distance(A, B):
    dim = len(A)
    d = 0
    for i in range(dim):
        d += (A[i]-B[i]) ** 2
    d = d ** 0.5
    return d


def getCenters(C):
    centers = []
    for c in C:
        center = getCenter(c)
        if center != 0:
            centers.append(center)
        else:
            centers.append(randomPoint())
    return centers


def randomPoint():
    global pointSet
    randomList = random.sample(range(len(pointSet)), 1)
    center = pointSet[randomList[0]]
    return center


def getCenter(c):
    n = len(c)
    if n <= 0:
        return 0
    dim = len(c[0])
    center = []
    for j in range(dim):
        t = 0
        for i in c:
            t += i[j]
        center.append(t/n)
    return center


dataFile = r"G:/study/dataMining/181213/聚类数据样本.csv"
pointSet = readDataFile(dataFile)
maxInter = 50
numOfClu = 4
cluster, centers = initCluster(pointSet, numOfClu)
for i in range(maxInter):
    cluster_last = getCluster(pointSet, centers)
    centers_n = getCenters(cluster_last)
    if ( isStatic(centers_n, centers) ):
        print("迭代次数:", i+1)
        break
    else:
        cluster = cluster_last
        centers = centers_n
else:
    print("到达最大迭代次数")
for i in range(len(cluster)):
    t = np.matrix(cluster[i])
    index_t = np.ones((len(cluster[i]), 1))
    index_t = index_t*i
    t = np.hstack((index_t, t))
    if i == 0:
        cluster_m = np.matrix(t)
    else:
        cluster_m = np.vstack((cluster_m, t))
# 可视化
tsne=TSNE()
cluster_2d = tsne.fit_transform(cluster_m[:, 1:5])  #进行数据降维,降成两维
# a=tsne.fit_transform(data_zs) #a是一个array,a相当于下面的tsne_embedding_
# tsne=tsne.embedding_ #转换数据格式
cluster_2d = np.matrix(cluster_2d)
cluster_2d = np.hstack((cluster_m[:, 0], cluster_2d))
pattern = ['r.', 'go', 'b*', 'y.', 'mo', 'k*']
for i in range(len(cluster_2d)):
    plt.plot(float(cluster_2d[i, 1]), float(cluster_2d[i, 2]), pattern[int(cluster_2d[i, 0])])
plt.show()
