#!/usr/bin/env python
#-*- coding:utf-8 -*-

import numpy as np

def loadExData():
    return [[1, 1, 1, 0, 0],
            [2, 2, 2, 0, 0],
            [1, 1, 1, 0, 0],
            [5, 5, 5, 0, 0],
            [1, 1, 0, 2, 2],
            [0, 0, 0, 3, 3],
            [0, 0, 0, 1, 1]]


# 相似度计算
def ecludSim(inA, inB):
    """欧几里德距离"""
    return 1.0 / (1.0 + np.linalg.norm(inA - inB))

def pearsSim(inA, inB):
    """皮尔逊相关度"""
    if len(inA) < 3:
        return 1.0
    return 0.5 + 0.5 * np.corrcoef(inA, inB, rowvar=0)[0][1]

def cosSim(inA, inB):
    """余弦相似度"""
    num = float(inA.T * inB)
    denom = np.linalg.norm(inA) * np.linalg.norm(inB)
    return 0.5 + 0.5 * (num / denom)
