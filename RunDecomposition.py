from fingerMerge import finger_merge
from random import randint, sample
class Run():
    def __init__(self,elems,mergeAlgo = finger_merge,monotonicity = "increasing") -> None:
        if len(elems) == 0:
            self.elems = elems
            self.min = float('inf')
            self.max = float('-inf')
            self.monotonicity = monotonicity
        else:
            i = 0
            while i+1 < len(elems) and elems[i] == elems[i+1]:
                i += 1
            if len(elems) <= 1 or i+1 == len(elems) or elems[i] > elems[i+1]:
                self.monotonicity = "decreasing"
                self.max = elems[0]
                self.min = elems[-1]
            else:
                self.monotonicity = "increasing"
                self.max = elems[-1]
                self.min = elems[0]
        self.elems = elems
        self.len = len(elems)
        self.mergeAlgo = mergeAlgo

    def mergeRuns(self,other):
        if self.monotonicity == "decreasing":
            if other.monotonicity == "decreasing": #both decreasing
                newElems = self.mergeAlgo(self.elems[::-1],other.elems[::-1])
            else:
                newElems = self.mergeAlgo(self.elems[::-1],other.elems)
        else:
            if other.monotonicity == "increasing": #both increasing
                newElems = self.mergeAlgo(self.elems,other.elems)
            else:
                newElems = self.mergeAlgo(self.elems,other.elems[::-1])
        return Run(newElems)

    def addRandomInts(self,nr):
        mi = int(min(self.elems))
        ma = int(max(self.elems))
        if ma-mi > 3:
            new_elems = [randint(mi+1,ma-1) for _ in range(nr)]
        else:
            new_elems = [randint(mi,ma) for _ in range(nr)]
        self.elems.extend(new_elems)
        self.elems = sorted(self.elems)
    
    def removeRandomInternalElems(self,nr):
        if len(self) <= 2:
            return False
        if len(self)-2 < nr:
            print(f"{len(self),nr,self.elems[1:-1] = }")
            raise Exception("Not enough elements to remove")
        newInternals = sample(self.elems[1:-1],len(self)-2-nr)
        self.elems[1:-1] = newInternals
        return True


    def reverse(self):
        self.elems = self.elems[::-1]
        if self.monotonicity == "decreasing":
            self.monotonicity = "increasing"
        else:
            self.monotonicity = "decreasing"

    def __sizeof__(self) -> int:
        return len(self.elems)

    def __len__(self):
        return len(self.elems)

    def __str__(self) -> str:
        return str(self.elems)

def RunDecomposition(L,mergeAlgo = finger_merge):
    if len(L) <= 2:
        return [Run(L,mergeAlgo = mergeAlgo)]
    i = 0
    j = 0
    runs = []
    while i < len(L):
        if L[i] >= L[i+1]: #decreasing run
            while L[i+j] >= L[i+j+1]:
                j += 1
                if i+j+1 >= len(L): #run goes to the end
                    runs.append(Run(L[i:],mergeAlgo = mergeAlgo))
                    return runs
        else: #increasing run
            while L[i+j] <= L[i+j+1]:
                j += 1
                if i+j+1 >= len(L): #run goes to the end
                    runs.append(Run(L[i:],mergeAlgo = mergeAlgo))
                    return runs
        runs.append(Run(L[i:i+j+1])) #slicing indexing needs + 1
        i += j + 1
        j = 0
        if i+j+1 >= len(L): #last slice is small
            runs.append(Run(L[i:],mergeAlgo = mergeAlgo))
            return runs
    return runs

def mergeTest():
    r1 = Run([1,2,3])
    r2 = Run([1,2,3])
    r3 = r1.mergeRuns(r2)
    print(r1,r2,"merge",r3)
    r1 = Run([1,2,3])
    r2 = Run([3,2,1])
    r3 = r1.mergeRuns(r2)
    print(r1,r2,"merge",r3)
    r1 = Run([3,2,1])
    r2 = Run([3,2,1])
    r3 = r1.mergeRuns(r2)
    print(r1,r2,"merge",r3)
    r1 = Run([3,2,1])
    r2 = Run([1,2,3])
    r3 = r1.mergeRuns(r2)
    print(r1,r2,"merge",r3)

def runDecompHardCases():
    print([4, 4, 3, 11, 7, 10, 8, 0, 12, 12, 6, 12, 9],"\n",[str(q) for q in RunDecomposition([4, 4, 3, 11, 7, 10, 8, 0, 12, 12, 6, 12, 9])])
    print([3, 3, 0, 3],"\n",[str(q) for q in RunDecomposition([3, 3, 0, 3])])