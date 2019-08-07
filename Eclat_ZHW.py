import time
class VerticalNSet:
    def __init__(self):
        self.itemSet = set()
        self.TIDSet = set()
        self.sup = 0


def initVerticalOneSet(data, minSup):
    VerticalOneSets = list()
    for i, transaction in enumerate(data):
        for j in transaction:
            for k in VerticalOneSets:
                if j in k.itemSet:
                    k.TIDSet.add(i)
                    k.sup = k.sup + 1
                    break
            else:
                vns = VerticalNSet()
                vns.itemSet.add(j)
                vns.TIDSet.add(i)
                vns.sup = 1
                VerticalOneSets.append(vns)
    r = list()
    for i in range(len(VerticalOneSets)):
        if VerticalOneSets[i].sup >= minSup:
            r.append(VerticalOneSets[i])
    VerticalOneSets = r
    return VerticalOneSets

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
verticalOneSets = initVerticalOneSet(data, minSup)
verticalNSets = verticalOneSets
trace = list()
if len(verticalNSets) > 0:
    trace.append(verticalNSets)
while len(verticalNSets) > 1:
    verticalNSets_next = list()
    for i in range(0,len(verticalNSets)-1):
        for j in range(i+1,len(verticalNSets)):
            itemSet_new = verticalNSets[i].itemSet | verticalNSets[j].itemSet
            if len(itemSet_new) == len(verticalNSets[i].itemSet) + 1:
                for k in verticalNSets_next:  # 判断是否已经存在了 如果不存在，执行else
                    if itemSet_new == k.itemSet:
                        break
                else:
                    TIDSet_new = verticalNSets[i].TIDSet & verticalNSets[j].TIDSet
                    if len(TIDSet_new) >= minSup:
                        vns = VerticalNSet()
                        vns.itemSet = itemSet_new
                        vns.TIDSet = TIDSet_new
                        vns.sup = len(vns.TIDSet)
                        verticalNSets_next.append(vns)
    if len(verticalNSets_next) > 0:
        trace.append(verticalNSets_next)
    verticalNSets = verticalNSets_next
for i in trace:  # 打印频繁项集
    for j in i:
        print(j.itemSet,j.sup)
t2 = time.time()
for i in range(0, len(trace)-1):  # 检查关联规则
    for j in trace[i]:
        for k in range(i+1, len(trace)):
            for h in trace[k]:
                if j.itemSet.issubset(h.itemSet):
                    if h.sup/j.sup >= minConf:
                        print(j.itemSet,"=>",h.itemSet-j.itemSet,h.sup/j.sup)

print("时间：",t2-t1)
