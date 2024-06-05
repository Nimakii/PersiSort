"""
Implementation of TimSort
"""
from random import random
from RunDecomposition import RunDecomposition
from fingerMerge import finger_merge
global total_comparisons
total_comparisons = 0

def merge12(Q):
    r1 = Q[-1]
    r2 = Q[-2]
    newR1 = r1.mergeRuns(r2)
    Q.pop()
    Q[-1] = newR1

def merge23(Q):
    r2 = Q[-2]
    r3 = Q[-3]
    newR2 = r2.mergeRuns(r3)
    r1 = Q.pop()
    Q[-1] = r1
    Q[-2] = newR2

def TimSort(X,cmp = False,mergeAlgo = finger_merge):
    Q = []
    runs = RunDecomposition(X,mergeAlgo = mergeAlgo)
    for r in runs:
        Q.append(r)
        while True:
            h = len(Q)
            if h >= 3 and Q[-1].len > Q[-3].len:
                merge23(Q)
            elif h >= 2 and Q[-1].len > Q[-2].len:
                merge12(Q)
            elif h >= 3 and Q[-1].len + Q[-2].len > Q[-3].len:
                merge12(Q)
            elif h >= 4 and Q[-2].len + Q[-3].len > Q[-4].len:
                merge12(Q)
            else:
                break
    while len(Q) > 1:
        merge12(Q)
    res = Q[-1].elems
    if not res[0]<=res[-1]:
        res = res[::-1]
    if cmp:
        global total_comparisons
        tot = total_comparisons
        total_comparisons = 0
        return res, tot
    else:
        return res 

def TimSortTest():
    X = [3,2,1,2,3,4,3,2]
    print("rundecomp",[str(r) for r in RunDecomposition(X)])
    print("timsort",TimSort(X))

def isSorted(lst):
    return all( a <= b for a,b in zip(lst,lst[1:]) )

def RandomTimSortTest(n,reps):
    for _ in range(reps):
        lst = [random()*(n) for _ in range(n)]
        if not isSorted(TimSort(lst)):
            return False, lst
    return True, []

def ManyRandomTimSortTests(m,reps):
    for n in range(1,m):
        res, lst = RandomTimSortTest(n,reps)
        if not res:
            print("not ok",lst,TimSort(lst))
            break
    print(f"{m = }, {reps = } succeded!")

def strDecomp(lst):
    return lst, [str(q) for q in RunDecomposition(lst)]

def TotalCmpTest():
    print(total_comparisons)
    TimSort([1,2,3,4])
    print(total_comparisons)
    total_comparisons = 0
    TimSort([4,3,2,1])
    print(total_comparisons)
    total_comparisons = 0
    TimSort([3,1,2,7,6,5,4])
    print(total_comparisons)
    total_comparisons = 0

if __name__ == "__main__":
    ManyRandomTimSortTests(500,25)
    pass