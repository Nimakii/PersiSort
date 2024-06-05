from random import shuffle,random

class Value:
    comparisons = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Value.comparisons += 1
        if type(other) == Value:
            return self.value < other.value
        else:
            return self.value < other

    def __ge__(self, other):
        Value.comparisons += 1
        if type(other) == Value:
            return self.value >= other.value
        else:
            return self.value >= other

    def __repr__(self):
        return repr(self.value)

    def __add__(self,other):
        if type(other) == Value:
            return Value(self.value+other.value)
        return Value(self.value+other)
    
    def __sub__(self,other):
        if type(other) == Value:
            return Value(self.value-other.value)
        return Value(self.value-other)
    
    def __abs__(self):
        return abs(self.value)

    def __int__(self):
        return int(self.value)

    def reset_count():
        Value.comparisons = 0

def set_name(name):
    """
    Sets the name for the decorated function
    Useful for plotting
    """
    def wrapper(f):
        f.__name__ = name
        return f
    return wrapper

@set_name("Isolated pairs")
def isolated_pairs(n, r):
    """
    @Author Casper
    Returns r runs of length >= 3, lengths uniformly at random
    """
    pivots = list(range(1, n - 2*r))
    shuffle(pivots)
    selected_pivots = [0] + sorted(pivots[:r - 1]) + [n - 2*r]
    cuts = [v + 2*i for i, v in enumerate(selected_pivots)]

    L = list(range(n))
    L_cut = [L[a:b] for a, b in zip(cuts, cuts[1:])]
    shuffle(L_cut)
    for i in range(1, r, 2):
        L_cut[i] = L_cut[i][::-1]
    return [v for run in L_cut for v in run]

@set_name("Uniformly random data")
def uniform_data(n,r):
    return [ random()*n for _ in range(n) ]

@set_name("Super nesting")
def super_nesting(n,r):
    lst = list(range(1,n//2))[::-1] + list(-x for x in range(n//2))
    elems_pr_run = n//r
    for i in range(r):
        lst[elems_pr_run *i : elems_pr_run *(i+1)] = [
        (-1)**i * x for x in lst[elems_pr_run*i : elems_pr_run *(i+1)]]
    return lst

@set_name("Ultra nesting")
def ultra_nesting(n,r):
    """
    X = [n/2,-n/2,n/2-1,-n/2+1,n/2-2,n/2+3,\dots,1,-1,0,-1+\epsilon,1+\epsilon,\dots,-n/2+\epsilon,n/2+\epsilon]$
    """
    eps = 0.01
    return [((-1)**i) * (n//2-i) for i in range(n)]

@set_name("Staircase")
def staircase(n,R):
    """
    Staircase with disjoint runs
    """
    lst = list(range(n))
    short = 3
    long = 2*n//R - short
    j = 0
    r = 0
    lists = []
    while True:
        if r % 2 == 0:
            lists.append( lst[j:j+short] )
            j += short
        else:
            lists.append( lst[j:j+long][::-1] )
            j += long
        r += 1
        if j > n:
            break
    res = []
    for ls in lists:
        res.extend(ls)
    return res

@set_name("Overlapping staircase")
def overlapping_staircase(n,R,o):
    """
    n elements in R runs with o overlap
    3 <= o <= (n//R)//2
    otherwise o doesn't make sense
    """
    lst = list(range(n))
    short = min(max(o,3),n//R) # force o into the correct interval
    short = o
    long = 2*n//R - short
    j = 0
    r = 0
    lists = []
    while True:
        if r % 2 == 0:
            lists.append( [x-r*o for x in lst[j:j+short]] )
            j += short
        else:
            lists.append( [x-r*o for x in lst[j:j+long][::-1]] )
            j += long
        r += 1
        if j > n:
            break
    res = []
    for ls in lists:
        res.extend(ls)
    while len(res) < n:
        res.append(res[-1]+1*(-1)**(R%2+1))
    return res

@set_name("TimSort Nemesis")
def TimSort_nemesis(n,r):
    """
    https://arxiv.org/pdf/1801.04641.pdf
    """
    if n <= 3:
        return list(range(n))
    if n % 2 == 0:
        n_ = n//2
        return TimSort_nemesis(n_,r) + TimSort_nemesis(n_-1,r) + [0]
    else:
        n_ = (n-1)//2
        return TimSort_nemesis(n_,r) + TimSort_nemesis(n_-1,r) + [0,1]


def randomized_datagen(x):
    repmap = { 
        isolated_pairs : True,
        uniform_data : True,
        staircase : False,
        super_nesting : False,
        ultra_nesting: False,
        TimSort_nemesis : False,
        overlapping_staircase : False
    }
    repmap.setdefault(False)
    return repmap[x]
def fixed_runs_possible(x):
    repmap = { 
        isolated_pairs : True,
        uniform_data : False,
        staircase : True,
        super_nesting : True,
        ultra_nesting: False,
        TimSort_nemesis : False,
        overlapping_staircase : True
    }
    repmap.setdefault(False)
    return repmap[x]

def overlapping_staircase_test(n,r,o):
    data = overlapping_staircase(n,r,o)
    test_datagens(n,[lambda x,y: overlapping_staircase(x,y,o)])
    plt.plot(list(range(len(data))),data,"o-")
    plt.show()

def all_data_distributions():
    return [uniform_data,staircase,isolated_pairs,super_nesting,TimSort_nemesis,ultra_nesting]

from PersiSort import extrema
from RunDecomposition import RunDecomposition
def test_datagens(n,gens):
    for datagen in gens:
        run_errs = 0
        extrema_errs = 0
        len_errs = 0
        fatal_errs = 0
        for r in range(3,n//10+1):
            try:
                data = datagen(n,r)
                runs = RunDecomposition(data)
                mins,maxs = extrema(data)
                if not ((len(mins) + len(maxs)) == r+1 ):
                    extrema_errs += 1
                if not ( len(runs) == r ):
                    run_errs += 1
                lens = sum(len(r) for r in runs)
                if not ( lens == n ):
                    #print("   ",lens,n)
                    len_errs += 1
            except:
                fatal_errs += 1
        print(datagen.__name__)
        print(" Extrema number errors",extrema_errs)
        print(" Run     number errors",run_errs)
        print(" Elem    number errors",len_errs)
        print("  Fatal errors",fatal_errs,"of",len(range(5,n//(10)+1)),"attempts")

import matplotlib.pyplot as plt
def visualize_datagen(datagen,n,r,marker='o'):
    data = datagen(n,r)
    plt.plot(list(range(len(data))),data,linestyle='-',marker=marker)
    return data

def test_datagen_fixed_n_r(n,datagen):
        run_errs = 0
        extrema_errs = 0
        len_errs = 0
        fatal_errs = 0
        rep = 0
        for r in range(3,n//3+1):
            for p in range(2,r):
                rep+=1
                try:
                    data = datagen(n,r,p)
                    runs = RunDecomposition(data)
                    mins,maxs = extrema(data)
                    if not ((len(mins) + len(maxs)) == r+1 ):
                        print("   Extrema error got:",(len(mins) + len(maxs)),"should get:",r+1)
                        extrema_errs += 1
                    if not ( len(runs) == r ):
                        print("   Run error     got:",len(runs),"should get:",r)
                        run_errs += 1
                    lens = sum(len(r) for r in runs)
                    if not ( lens == n ):
                        print("   Element error got:",lens,"should get:",n)
                        len_errs += 1
                except:
                    fatal_errs += 1
        print(datagen.__name__)
        print(" Extrema number errors",extrema_errs)
        print(" Run     number errors",run_errs)
        print(" Elem    number errors",len_errs)
        print("  Fatal errors",fatal_errs,"of",rep,"attempts")

if __name__ == "__main__":
    data = overlapping_staircase(20000,300,60)
    plt.plot(list(range(len(data))),data,linestyle='-',marker='o')
    plt.show()
    exit()
    pass