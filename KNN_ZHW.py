import numpy as np
import matplotlib.pyplot as plt


def KNN(data, testData,k):
    # testData = np.hstack( (testData, np.ones(len(testData),1)) )
    pred = list()
    for i, pointi in enumerate(testData):
        distences = list()
        for j, pointj  in enumerate(data):
            distences.append(getD(pointj[0: -1], pointi))
        sortedDistIndex = np.argsort(distences)
        neighborCate = list()
        for j in range(k):
            neighborCate.append(data[sortedDistIndex[j],-1])
        # neighborCate = map(distences.index, heapq.nsmallest(k, distences))
        cate = neighborCate[0]
        maxNum = 0
        for j in neighborCate:
            if neighborCate.count(j) > maxNum:
                maxNum = neighborCate.count(j)
                cate = j
        pred.append(cate)
    return pred



def getD(v1,v2):
    D = 0
    for i in range(len(v1)):
        D = D + (v1[i]-v2[i]) ** 2
    D = D ** 0.5
    return D


wmdata3_o = [
    [0.697, 0.46, 1],
    [0.774, 0.376, 1],
    [0.634, 0.264, 1],
    [0.608, 0.318, 1],
    [0.556, 0.215, 1],
    [0.403, 0.237, 1],
    [0.481, 0.149, 1],
    [0.437, 0.211, 1],
    [0.666, 0.091, 0],
    [0.243, 0.267, 0],
    [0.245, 0.057, 0],
    [0.343, 0.099, 0],
    [0.639, 0.161, 0],
    [0.657, 0.198, 0],
    [0.36, 0.37, 0],
    [0.593, 0.042, 0],
    [0.719, 0.103, 0]
]
k = 3
data =np.array(wmdata3_o)
testData = np.array([[0.56, 0.19], [0.32, 0.29]])
pred = KNN(data, testData, k)
pattern = ['r*', 'g*', 'b*', 'y*', 'm*', 'k*']
pattern_test = ['ro', 'go', 'bo', 'yo', 'mo', 'ko']
for i, point in enumerate(data):
    plt.plot(point[0], point[1], pattern[int(point[2])])
for i, point in enumerate(testData):
    plt.plot(point[0], point[1], pattern_test[int(pred[i])])
plt.show()
