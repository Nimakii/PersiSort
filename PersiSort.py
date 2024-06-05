"""
New sorting algorithm based upon Persistent homology.
"""
from random import random, shuffle

def isSorted(A):
    return all( ai <= aip for ai,aip in zip(A,A[1:]))

def extrema(lst: list):
    minimums = []
    maximums = []
    if len(lst) == 0:
        return [], []
    if len(lst) == 1: #favors minimum
        return lst , []
    if len(lst) == 2:
        one,two = lst
        if one <= two:
            return [one] , [two]
        else:
            return [two] , [one]
    i = 0
    j = 0
    l = 0
    while lst[l] == lst[l+1]:
        l+=1
    if lst[l] <= lst[l+1]:
        minimums.append(0)
    else:
        maximums.append(0)
    lastRunDecr = False
    lastRunIncr = False
    while i < len(lst):
        if lst[i] >= lst[i+1]: #decreasing run
            if lastRunDecr:
                maximums.append(i)
            else:
                lastRunDecr = True
                lastRunIncr = False
            while lst[i+j] >= lst[i+j+1]:
                j += 1
                if i+j+1 >= len(lst): #run goes to the end
                    minimums.append(len(lst)-1)
                    return minimums , maximums
            minimums.append(i+j)
        else: #increasing run
            if lastRunIncr:
                minimums.append(i)
            else:
                lastRunDecr = False
                lastRunIncr = True
            while lst[i+j] <= lst[i+j+1]:
                j += 1
                if i+j+1 >= len(lst): #run goes to the end
                    maximums.append(len(lst)-1)
                    return minimums , maximums
            maximums.append(i+j)
        i += j + 1
        j = 0
        if i+j+1 >= len(lst): #last run is small
            if lst[-2] <= lst[-1]:
                maximums.append(len(lst)-1)
                break
            else:
                minimums.append(len(lst)-1)
                break
    return minimums , maximums

def argmin(i1,i2,lst):
    if lst[i1] <= lst[i2]:
        return i1
    return i2

def argmax(i1,i2,lst):
    if lst[i1] >= lst[i2]:
        return i1
    return i2
            
def Minpairings(mins,maxes,elems):
    minpairings = []
    # handle start
    if len(maxes) == 0:
        print("0 maxes error")
    if mins[0] < maxes[0]: # first run incraesing
        minpairings.append( (mins[0] , maxes[0]) ) # mins[0] only has 1 option
        offset = 0
    else: # first run decrasing
        minpairings.append( (mins[0] , argmin(maxes[0],maxes[1],elems)) )
        offset = 1

    # handle end
    if mins[-1] < maxes[-1]: # last run increasing
        minpairings.append( (mins[-1] , argmin(maxes[-2],maxes[-1],elems)) )
    else:
        minpairings.append( (mins[-1] , maxes[-1]) )

    # handle middle
    for i,m in enumerate(mins[1:-1]):
        if i+1 >= len(maxes):
            continue
        #minpairings.append( (m , argmin(maxes[i],maxes[i+1],elems)) )
        minpairings.append( (m , argmin(maxes[i+offset],maxes[i+1+offset],elems)) )
    
    return minpairings

def Maxpairings(mins,maxes,elems): #O(r)
    maxpairings = []
    # handle start
    if mins[0] < maxes[0]: # first run incraesing
        maxpairings.append( (maxes[0] , argmax(mins[0],mins[1],elems)) ) 
        offset = 1
    else: # first run decrasing
        maxpairings.append( (maxes[0] , mins[0]) ) # maxes[0] only has 1 option
        offset = 0

    # handle end
    if mins[-1] < maxes[-1]: # last run increasing
        maxpairings.append( (maxes[-1] , mins[-1]) )
    else:
        maxpairings.append( (maxes[-1] , argmax(mins[-2],mins[-1],elems)) )

    # handle middle
    for i,m in enumerate(maxes[1:-1]):
        maxpairings.append( (m , argmax(mins[i+offset],mins[i+1+offset],elems)) )
    
    return maxpairings

def pairings(minpairings,maxpairings):
    revMaxPairs = [ (b,a) for a,b in maxpairings ]
    res = set( pair for pair in revMaxPairs if pair in minpairings )
    return [*set(res)]

def persistencePairing(lst,mins,maxs):
    if len(mins) == len(maxs) == 1:
        return list(zip(mins,maxs))
    if len(mins) + len(maxs) == 3:
        if len(mins) == 1:
            maxi = argmin(maxs[0],maxs[1],lst)
            return [(mins[0] , maxi)]
        return [(argmax(mins[0],mins[1],lst) , maxs[0])]
    return pairings(Minpairings(mins,maxs,lst), Maxpairings(mins,maxs,lst))

def myprint(bol,*str):
    if bol:
        print(str)

def Oh1PersistencePairing(lst,newextremas,oldpairs,prints = False,hotfix = True):
    """
    Find new persistence pairs by looking at neighbours
    Newextremas are updated after merging around pairings, if not there are errors
    returns new persistence pairings, in amortized O(1)

    The constant can be improved by remembering proposals such that these can be reused
    """
    n = len(lst)
    mins,maxs = newextremas
    myprint(prints,"Starting Oh1 PP")
    if len(mins) == len(maxs) == 1:
        return list(zip(mins,maxs))
    if len(mins) + len(maxs) == 3:
        if len(mins) == 1:
            maxi = argmin(maxs[0],maxs[1],lst)
            return [(mins[0] , maxi)]
        return [(argmax(mins[0],mins[1],lst) , maxs[0])]
    if len(mins) + len(maxs) <= 8:
        return persistencePairing(lst,mins,maxs)

    myprint(prints,"mins",mins)
    myprint(prints,"maxs",maxs)
    newpairs = []
    max_seen = set()
    min_seen = set()
    for mini,maxi in oldpairs:
        myprint(prints,"mini,maxi",mini,maxi)
        if mini < maxi: # pair was increasing and is now contained in a decreasing run
            # boundaries of the DECREASING run
            containing_run_start,cmaxindex = max((x,i) for i,x in enumerate(maxs) if x <= maxi)
            containing_run_end,cminindex = min((x,i) for i,x in enumerate(mins) if x >= mini)
            myprint(prints,containing_run_start,cmaxindex , containing_run_end,cminindex)
            
            if cmaxindex in max_seen: #don't repeat work
                continue
            else:
                max_seen.add(cmaxindex)
                max_seen.discard(0)
                max_seen.discard(n-1)
            if cminindex in min_seen: #don't repeat work
                continue
            else:
                min_seen.add(cminindex)
                min_seen.discard(0)
                min_seen.discard(n-1)
            
            
            # check if the smoothing of mini and maxi gives rise to any new pairs
            # it can give 0-2 new pairs
            
            # handle START
            if containing_run_start == 0:
                myprint(prints,"decr, start")
                if lst[0] <= lst[maxs[1]]:
                    newpairs.append((mins[0],0))

                elif lst[mins[0]] > lst[mins[1]]: # lst[0] > lst[maxs[1]] from before
                    newpairs.append((mins[0],maxs[1]))
            
            # handle END
            elif containing_run_end == n-1:
                myprint(prints,"decr, end")
                if lst[-1] > lst[mins[-2]]:
                    newpairs.append((n-1,containing_run_start))

                elif lst[maxs[-1]] <= lst[maxs[-2]]: # lst[-1] <= lst[mins[-1]]
                    newpairs.append((mins[-2],maxs[-1]))

            # handle middle
            else:
                myprint(prints,"decr, middle")
                # new pair over smoothed area, i.e. new box contains old box
                min_propose_max = lst[containing_run_start] <= lst[maxs[cmaxindex+1]]
                max_propose_min = lst[containing_run_end] > lst[mins[cminindex-1]]
                if  max_propose_min and min_propose_max:
                    newpairs.append((containing_run_end,containing_run_start))
                    continue # in this case this will be the only pairing
                    # but in the next cases, both can happen at the same time
                
                # check pair to the left
                if (not max_propose_min) and \
                    (cmaxindex == 0 or \
                    lst[containing_run_start] <= lst[maxs[cmaxindex-1]]):
                    newpairs.append((mins[cminindex-1],containing_run_start))
                
                # check pair to the right
                if (not min_propose_max) and \
                    (cminindex == len(mins)-1 or \
                    lst[containing_run_end] > lst[mins[cminindex+1]]):
                    newpairs.append((containing_run_end,maxs[cmaxindex+1]))
                    

        else: # pair is now contained in an increasing run
            # boundaries of the INCREASING run
            containing_run_start,cminindex = max((x,i) for i,x in enumerate(mins) if x <= mini)
            containing_run_end,cmaxindex = min((x,i) for i,x in enumerate(maxs) if x >= maxi)
            myprint(prints,containing_run_start,cmaxindex , containing_run_end,cminindex)
            if cmaxindex in max_seen: #don't repeat work
                continue
            else:
                max_seen.add(cmaxindex)
                max_seen.discard(0)
                max_seen.discard(n-1)
            if cminindex in min_seen: #don't repeat work
                continue
            else:
                min_seen.add(cminindex)
                min_seen.discard(0)
                min_seen.discard(n-1)
            
            # check if the smoothing of mini and maxi gives rise to any new pairs
            # it can give 0-2 new pairs

            # handle START
            if containing_run_start == 0:
                myprint(prints,"incr, start")
                if lst[0] > lst[mins[1]]:
                    newpairs.append((0,maxs[0]))
                    continue
                elif lst[maxs[0]] <= lst[maxs[1]]: # lst[0] <= lst[mins[1]]
                    newpairs.append((mins[1],maxs[0]))
                    continue

            # handle END
            elif containing_run_end == n-1:
                myprint(prints,"incr, end")
                if lst[-1] <= lst[maxs[-2]]:
                    newpairs.append((containing_run_start,n-1))

                elif lst[mins[-1]] > lst[mins[-2]]: # lst[-1] > lst[maxs[-1]]
                    newpairs.append((mins[-1],maxs[-2]))

            # handle middle
            else:
                myprint(prints,"incr, middle")
                # new pair over smoothed area, i.e. new box contains old box
                min_propose_max = lst[containing_run_end] <= lst[maxs[cmaxindex-1]]
                max_propose_min = lst[containing_run_start] > lst[mins[cminindex+1]]
                if  max_propose_min and min_propose_max:
                    newpairs.append((containing_run_start,containing_run_end))
                    continue # in this case this will be the only pairing
                    # but in the next cases, both can happen at the same time
                
                # check pair to the left
                if (not max_propose_min) and \
                    (cmaxindex == len(maxs)-1 or \
                    lst[containing_run_end] <= lst[maxs[cmaxindex+1]]):
                    newpairs.append((mins[cminindex+1],containing_run_end))
                
                # check pair to the right
                if (not min_propose_max) and \
                    (cminindex == 0 or \
                    lst[containing_run_start] > lst[mins[cminindex-1]]):
                    newpairs.append((containing_run_start,maxs[cmaxindex-1]))
        myprint(prints,"newpairs",newpairs)
    if (not newpairs) and hotfix: # dirty
        # there is an issue where the new pair isn't discovered
        # this issue goes past my unit tests
        # the simple solution is to run the linear pairing method
        myprint(prints,lst,mins,maxs,newextremas,oldpairs)
        return persistencePairing(lst,mins,maxs)
    # return newpairs
    # some duplicates can appear
    res = list(set(newpairs))
    if len(res) == 0:
        fakepairs = []
        if lst[0] < lst[1]:
            #first run incr
            fakepairs.append([1,0])
        else:
            fakepairs.append([0,1])
        if lst[-1] > lst[-2]:
            #last run incr
            fakepairs.append([n-1,n-2])
        else:
            fakepairs.append([n-2,n-1])
        return Oh1PersistencePairing(lst,newextremas,[],prints=prints,hotfix=hotfix)
    return res




from fingerMerge import finger_merge, finger_merge_22

def finger_merge_3(A,B,C):
    return finger_merge_22(A,B,C)

def printIfDebug(strng,debug):
    if debug:
        print(strng)

def threeWayMergeFingerMerge(lst,mini,maxi,current_extrema):
    mins,maxs = current_extrema
    debug = False
    #printIfDebug(f"3waymerge: {unperturbe(lst)}\n  {mini,maxi,len(lst) = }\n  {mins,maxs = }",debug)
    
    #handle start
    if mini == 0: #incr decr
        #minipp = mins[mins.index(mini)+1]
        minipp = mins[1]
        lst[0:minipp+1] = finger_merge(lst[:maxi+1],lst[maxi+1:minipp+1][::-1])[::-1]
        #printIfDebug(f"  Merged start mini: {unperturbe(lst)}",debug)
        return lst
    if maxi == 0: #decr incr
        #maxipp = maxs[maxs.index(maxi)+1]
        maxipp = maxs[1]
        lst[0:maxipp+1] = finger_merge((lst[:mini+1])[::-1],lst[mini+1:maxipp+1])
        #printIfDebug(f"  Merged start maxi: {unperturbe(lst)}",debug)
        return lst

    #handle end
    if mini == len(lst)-1: #incr decr
        #minimm = mins[mins.index(mini)-1]
        minimm = mins[-2]
        lst[minimm:] = finger_merge(lst[minimm:maxi],lst[maxi:][::-1])
        #printIfDebug(f"  Merged end mini: {unperturbe(lst)}",debug)
        return lst
    if maxi == len(lst)-1: #decr incr
        #maximm = maxs[maxs.index(maxi)-1]
        maximm = maxs[-2]
        lst[maximm:] = finger_merge(lst[mini:],lst[maximm:mini][::-1])[::-1]
        #printIfDebug(f"  Merged end maxi: {unperturbe(lst)}",debug)
        return lst

    #handle middle
    if mini < maxi: #decr incr decr
        maximm = maxs[maxs.index(maxi)-1]
        minipp = mins[mins.index(mini)+1]
        lst[maximm:minipp+1] = finger_merge_3(lst[maximm:mini][::-1],lst[mini:maxi],lst[maxi:minipp+1][::-1])[::-1]
        #printIfDebug(f"  Merged middle mini<maxi: {unperturbe(lst)}",debug)
        return lst
    if mini > maxi: #incr decr incr
        minimm = mins[mins.index(mini)-1]
        maxipp = maxs[maxs.index(maxi)+1]
        lst[minimm:maxipp+1] = finger_merge_3(lst[minimm:maxi],lst[maxi:mini][::-1],lst[mini:maxipp+1])
        #printIfDebug(f"  Merged middle maxi < mini: {unperturbe(lst)}",debug)
        return lst


def check_TopoSortCompleted(lst,current_extrema):
    mins,maxs = current_extrema
    return (mins[0],maxs[0]) in ((0,len(lst)-1),(len(lst)-1,0))

def recalculate_extrema(current_extrema,persistencePairs,n):
    mins, maxs = current_extrema
    usedmins, usedmaxs = list(zip(*persistencePairs))
    new_extrema = [ [mi for mi in mins if not mi in usedmins] ,
                    [ma for ma in maxs if not ma in usedmaxs]  ]
    if 0 in usedmins:
        new_extrema[1] = [0] + new_extrema[1]
    elif 0 in usedmaxs:
        new_extrema[0] = [0] + new_extrema[0]
    if n-1 in usedmins:
        new_extrema[1].append(n-1)
    elif n-1 in usedmaxs:
        new_extrema[0].append(n-1)
    prnt = False
    if prnt:
        print("Recalculate extrema")
        print(usedmins)
        print(usedmaxs)
        print(persistencePairs)
        print(new_extrema)
    return new_extrema

def remove_extrema(current_extrema,mini,maxi,n):
    mins, maxs = current_extrema
    new_extrema = [ [mi for mi in mins if not mi == mini] ,
                    [ma for ma in maxs if not ma == maxi]  ]
    if 0 == mini:
        new_extrema[1] = [0] + new_extrema[1]
    elif 0 == maxi:
        new_extrema[0] = [0] + new_extrema[0]
    if n-1 == mini:
        new_extrema[1].append(n-1)
    elif n-1 == maxi:
        new_extrema[0].append(n-1)
    return new_extrema

def shuffled(lst):
    shuffle(lst)
    return lst

def persistencepair_levels(lst):
    """
    Returns all persistence pairs, ordered by level
    """
    n = len(lst)
    current_extrema = extrema(lst)
    persistencePairs = persistencePairing(lst,*current_extrema)
    level = 0
    pairs = [[] for _ in range(n+1)]
    while not check_TopoSortCompleted(lst,current_extrema):
        for mini,maxi in persistencePairs:
            pairs[level].append((mini,maxi))
            current_extrema = remove_extrema(current_extrema,mini,maxi,n)
        persistencePairs = Oh1PersistencePairing(lst,current_extrema,persistencePairs)
        level += 1
    pairs = [p for p in pairs if p]
    return pairs

def sort_persistence(pairs,lst):
    return sorted(pairs,key=lambda x: abs(lst[x[0]]-lst[x[1]]))

def PersiSort_base(inp,threeWayMerge = threeWayMergeFingerMerge):
    lst = inp[:]
    n = len(lst)
    current_extrema = extrema(lst)
    persistencePairs = persistencePairing(lst,*current_extrema)
    while True:
        if check_TopoSortCompleted(lst,current_extrema):
            if lst[0] >= lst[-1]: #reverse sorted
                lst = lst[::-1]
            return lst
        for mini, maxi in persistencePairs: # this can be parallelised
            lst = threeWayMerge(lst,mini,maxi,current_extrema)
            current_extrema = remove_extrema(current_extrema,mini,maxi,n)
        persistencePairs = Oh1PersistencePairing(lst,current_extrema,persistencePairs)
        #persistencePairs = persistencePairing(lst,*current_extrema)
def PersiSort(inp):
    """
    Proof of concept implementation.
      O(1) persistence pairing (amortized) doesn't work on the TimsortNemesis distribution
      without perturbation. The error likely arises when extrmal values come in triples say
      ...,2,1,0,0,0,1,2,... which of these 0s define the minimum?
    """
    data = [l+random()/1000 for l in inp]
    sorted_data = PersiSort_base(data)
    return [int(d) for d in sorted_data]

from DataGenerators import ultra_nesting
def perspairtest():
    lst = [x+15 for x in ultra_nesting(25,0)]
    current_extrema = extrema(lst)
    persistencePairs = persistencePairing(lst,*current_extrema)
    print("lst=",list(enumerate(lst)))
    print("E=",current_extrema)
    print("MinProposals",Minpairings(*current_extrema,lst))
    print("MaxProposals",Maxpairings(*current_extrema,lst))
    print("pairs=",persistencePairs)

def isSorted(data):
    return all (di <= dip for di,dip in zip(data,data[1:]))

from DataGenerators import all_data_distributions
def stress_test(datagens):
    for logn in range(4,15):
        for logr in range(2,logn-2):
            for datagen in datagens:
                data = datagen(2**logn,2**logr)
                if not isSorted(PersiSort(data)):
                    print("error",datagen)
        print(f"{2**logn} ok")

if __name__ == "__main__":
    #perspairtest()
    stress_test(all_data_distributions())
