"""
@author Sebastian Wild
https://colab.research.google.com/drive/13jJDr7dcEz2Ub48TzOT-DaJYCNc5UduR?usp=sharing#scrollTo=_BYEaBUGxTmd

"""
import math


MERGE_COST = 0

from fingerMerge import finger_merge

def merge(run1, run2):
    return finger_merge(run1,run2)


def merge_inplace(a, i, m, j):
    #print(f'Merge({i}, {m}, {j})')
    global MERGE_COST
    MERGE_COST += j-i
    a[i:j] = merge(a[i:m], a[m:j])


def extend_run(a, i):
    """Extend a run in a list"""
    if i == len(a) - 1:
        return i + 1
    j = i + 1
    if a[i] <= a[j]:
        while j < len(a) and a[j - 1] <= a[j]:
            j += 1
    else:
        while j < len(a) and a[j - 1] > a[j]:
            j += 1
        a[i:j] = reversed(a[i:j])
    return j


def extend_run_increasing_only(a, i):
    """Extend a run in a list"""
    if i == len(a) - 1:
        return i + 1
    j = i + 1
    while j < len(a) and a[j - 1] <= a[j]:
        j += 1
    return j

def power(run1, run2, n):
    i1 = run1[0]; n1 = run1[1]
    i2 = run2[0]; n2 = run2[1]
    assert i1 >= 0
    assert i2 == i1 + n1
    assert n1 >= 1 and n2 >= 1
    assert i2 + n2 <= n
    a = (i1 + n1/2) / n
    b = (i2 + n2/2) / n
    l = 0
    while math.floor(a * 2**l) == math.floor(b * 2**l):
        l += 1
    return l


def power_fast(run1, run2, n):
    # Compute the "power" of the run boundary.
    # Given are two adjacent runs from a list of total length n.
    # See listsort.txt for details; the code follows the CPython implementation.
    i1 = run1[0]; n1 = run1[1]
    i2 = run2[0]; n2 = run2[1]
    # a' = i1 + l1/2
    # b' = i2 + l2/2 = a' + (l1 + l2)/2
    a = 2 * i1 + n1       # 2 * a'
    b = a + n1 + n2       # 2 * b'
    l = 0
    while True:
        l += 1
        if a >= n:
            assert b >= a
            a -= n
            b -= n
        elif b >= n:
            break
        assert a < b < n
        a <<= 1
        b <<= 1
    return l


def merge_topmost_2(a, runs):
    assert len(runs) >= 2
    Y = runs[-2]
    Z = runs[-1]
    assert Z[0] == Y[0] + Y[1]
    merge_inplace(a, Y[0], Z[0], Z[0] + Z[1])
    runs[-2] = (Y[0], Y[1] + Z[1], Y[2]) #min(Y[2], Z[2]))
    del runs[-1]


def powersort(a, extend_run=extend_run):
    """
    Sort a list using powersort.
    This is a slick variant for managing the stack
    (no need to update the power inside the stack), but it is conceptually
    not exactly the same as the CPython print('Merge cost:', MERGE_COST)implementation.
    This stores the run-boundary power in the right run, CPython stores it
    in the left run.
    """
    n = len(a)
    i = 0
    runs = []
    j = extend_run(a, i)
    runs.append((i, j - i, 0))
    i = j
    while i < n:
        j = extend_run(a, i)
        p = power(runs[-1], (i,j-i), n)
        while p <= runs[-1][2]:
            merge_topmost_2(a, runs)
        runs.append((i,j-i,p))
        i = j
    while len(runs) >= 2:
        merge_topmost_2(a, runs)
    return a
