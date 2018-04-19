#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys

import numpy as np


def read_input(file):
    for line in file:
        yield line.rstrip()

inp = read_input(sys.stdin)
mapperOut = [line.split('\t') for line in inp]
cumVal = 0.0
cumSumSq = 0.0
cumN = 0.0
for instance in mapperOut:
    nj = float(instance[0])
    cumN += nj
    cumVal += nj * float(instance[1])
    cumSumSq += nj * float(instance[2])
mean = cumVal / cumN
varSum = (cumSumSq - 2 * mean * cumVal + cumN * mean * mean) / cumN
print("%d\t%f\t%f" % (cumN, mean, varSum))
print("report: still alive", file=sys.stderr)
