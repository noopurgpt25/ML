import math
import scipy.spatial
import scipy.stats
import numpy as np
import csv

def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)

def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    return diffprod / math.sqrt(xdiff2 * ydiff2)


# a = [15, 12, 8, 8, 7, 7, 7, 6, 5, 3]
# b = [10, 25, 17, 11, 13, 17, 20, 13, 9, 15]
# from scipy.stats import linregress
# slope, intercept, r_value, p_value, std_er = linregress(a,b)
# print p_value


def manhattan(x,y):
    return scipy.spatial.distance.cityblock(x,y)

def mode(a):
    return scipy.stats.mstats.mode(a)

def t_test(data):
    return scipy.stats.ttest_1samp(data,49)

