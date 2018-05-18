#!/usr/bin/env python
#-*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt


class matchrow:
    def __init__(self, row, allnum=False):
        if allnum:
            self.data = [float(row[i]) for i in range(len(row)-1)]
        else:
            self.data = row[0:len(row)-1]
        self.match = int(row[len(row)-1])

def loadmatch(f, allnum=False):
    rows = []
    with open(f) as f:
        lines = f.readlines()
        for line in lines:
            rows.append(matchrow(line.split(','), allnum))
    return rows


# 可视化
def plotagematches(rows):
    xdm, ydm = [r.data[0] for r in rows if r.match == 1], [r.data[1] for r in rows if r.match == 1]
    xdn, ydn = [r.data[0] for r in rows if r.match == 0], [r.data[1] for r in rows if r.match == 0]

    plt.plot(xdm, ydm, 'go')
    plt.plot(xdn, ydn, 'r+')

    plt.show()


## 基本的线性分类

# 计算分类的均值点
def lineartrain(rows):
    averages = {}
    counts = {}

    for row in rows:
        # 得到该坐标所属的分类
        cl = row.match

        averages.setdefault(cl, [0.0] * (len(row.data)))
        counts.setdefault(cl, 0)

        # 将该坐标点加入average中
        for i in range(len(row.data)):
            averages[cl][i] += float(row.data[i])

        # 记录每个分类中有多少坐标点
        counts[cl] += 1

    # 将总和除以计数值以求得平均值
    for cl, avg in averages.items():
        for i in range(len(avg)):
            avg[i] /= counts[cl]

    return averages

# 求向量点积
def dotproduct(v1, v2):
    return sum([v1[i] * v2[i] for i in range(len(v1))])

# 利用点积结果符号来确定分类
def dpclassify(point, avgs):
    b = (dotproduct(avgs[1], avgs[1]) - dotproduct(avgs[0], avgs[0])) / 2
    y = dotproduct(point, avgs[0]) - dotproduct(point, avgs[1]) + b
    if y > 0:
        return 0
    else:
        return 1

# 将数据转换为是否问题
def yesno(v):
    if v == 'yes':
        return 1
    elif v == 'no':
        return -1
    else:
        return 0

# 得到匹配项的数量
def matchcount(interest1, interest2):
    l1 = interest1.split(':')
    l2 = interest2.split(':')
    x = 0
    for v in l1:
        if v in l2:
            x += 1
    return x


# 计算距离
def miledistance(a1, a2):
    return 0

# 构造新的数据集
def loadnumerical():
    oldrows = loadmatch('matchmaker.csv')
    newrows = []
    for row in oldrows:
        d = row.data
        data = [float(d[0]), yesno(d[1]), yesno(d[2]),
                float(d[5]), yesno(d[6]), yesno(d[7]),
                matchcount(d[3], d[8]),
                milesdistance(d[4], d[9]),
                row.match]
        newrows.append(matchrow(data))
    return newrows

# 数据缩放
def scaledata(rows):
    low = [999999999.0] * len(rows[0].data)
    high = [-999999999.0] * len(rows[0].data)
    # 寻找最大值和最小值
    for row in rows:
        d = row.data
        for i in range(len(d)):
            if d[i] < low[i]:
                low[i] = d[i]
            if d[i] > high[i]:
                high[i] = d[i]

    # 对数据进行缩放处理的函数
    def scaleinput(d):
        return [(d.data[i] - low[i]) / (high[i] - low[i])
                   for i in range(len(row))]

    # 对所有数据进行缩放处理
    newrows = [matchrow(scaleinput(row.data)+[row.match])
                   for row in rows]

    # 返回新的数据和缩放处理函数
    return newrows, scaleinput
