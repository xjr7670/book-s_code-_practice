#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import random
import math


people = [
        ('Seymour', 'BOS'),
        ('Franny', 'DAL'),
        ('Zooey', 'CAK'),
        ('Walt', 'MIA'),
        ('Buddy', 'ORD'),
        ('Les', 'OMA')
        ]

destination = 'LGA'

flights = {}

with open('schedule.txt') as f:
    flight_text = f.readlines()

for line in flight_text:
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights.setdefault((origin, dest), [])

    # 将航班详情添加到航班列表中
    flights[(origin, dest)].append((depart, arrive, int(price)))

def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]

def printschedule(r):
    for d in range(len(r)//2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][r[2*d]]
        ret = flights[(destination, origin)][r[2*d+1]]
        print('%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2]))

def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60

    for d in range(len(sol)//2):
        # 得到往返航班和返程航班
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(destination, origin)][int(sol[2*d+1])]

        # 总价格等于所有往程航班和返程航班价格之和
        totalprice += outbound[2]
        totalprice += returnf[2]

        # 记录最晚到达时间和最早离开时间
        if latestarrival < getminutes(outbound[1]):
            latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]):
            earliestdep = getminutes(returnf[0])

    # 每个人必须在机场等待直到最后一个人到达为止
    # 他们也必须在相同时间到达，并等候他们的返程航班
    totalwait = 0
    for d in range(len(sol)//2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[2*d])]
        returnf = flights[(destination, origin)][int(sol[2*d+1])]
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep

    if latestarrival > earliestdep:
        totalprice += 50

    return totalprice + totalwait


# 随机搜索
def randomoptimize(domain, costf):
    best = 999999999
    bestr = None
    for i in range(1000):
        # 创建一个随机解
        r = [random.randint(domain[i][0], domain[i][1])
                for i in range(len(domain))]
        # 得到成本
        cost = costf(r)
        
        # 与到目前为止的最优解进行比较
        if cost < best:
            best = cost
            bestr = r

    return r

# 爬山法
def hillclimb(domain, costf):
    # 创建一个随机解
    sol = [random.randint(domain[i][0], domain[i][1])
            for i in range(len(domain))]

    # 主循环
    while 1:
        # 创建相邻解的列表
        neighbors = []
        for j in range(len(domain)):
            # 在每个方向上相对于原值偏离一点
            if sol[j] > domain[j][0]:
                neighbors.append(sol[0:j] + [sol[j] - 1] + sol[j+1:])
            if sol[j] < domain[j][1]:
                neighbors.append(sol[0:j] + [sol[j] + 1] + sol[j+1:])

        # 在相邻解中寻找最优解
        current = costf(sol)
        best = current
        for j in range(len(neighbors)):
            cost = costf(neighbors[j])
            if cost < best:
                best = cost
                sol = neighbors[j]

        # 如果没有更好的解，则退出循环
        if best == current:
            break

    return sol

# 模拟退火算法
def annealingoptimize(domain, costf, T=10000.0, cool=0.95, step=1):
    # 随机初始化值
    vec = [random.randint(domain[i][0], domain[i][1])
            for i in range(len(domain))]

    while T > 0.1:
        # 选择一个索引值
        i = random.randint(0, len(domain)-1)

        # 选择一个改变索引值的方向
        direct = random.randint(-step, step)

        # 创建一个代表题解的新列表，改变其中一个值
        vecb = vec[:]
        vecb[i] += direct               # 每次改变一个单位
        if vecb[i] < domain[i][0]:      #
            vecb[i] = domain[i][0]      # 保存最小值
        elif vecb[i] > domain[i][1]:    #
            vecb[i] = domain[i][1]      #

        # 计算当前成本和新的成本
        ea = costf(vec)
        eb = costf(vecb)

        # 它是更好的解吗？或者是趋向最优解的可能的临界解吗？
        if (eb < ea or random.random() < pow(math.e, -(eb-ea)/T)):
            vec = vecb

        # 降低温度
        T = T * cool
    return vec
