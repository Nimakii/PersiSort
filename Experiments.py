from boxplot import confidence_boxplot
import matplotlib.pyplot as plt
from DataGenerators import Value
from datetime import date
from time import time
from DataGenerators import *

def confidence_timvstopo_varyRuns(elements,runrange,datagenerator,sortingfunctions,reps=100):
    R = list(runrange)
    total_comparisons = [[] for _ in range(len(sortingfunctions))]
    print("Starting runs for",datagenerator.__name__)
    for r in R:
        current_comparisons = [[] for _ in range(len(sortingfunctions))]
        for _ in range(100):
            lst = lst = [Value(y) for y in datagenerator(elements,r)]
            for i,sortfunc in enumerate(sortingfunctions):
                Value.reset_count() #some data generators sort things to build runs
                sortfunc(lst)
                current_comparisons[i].append(Value.comparisons)
        for i,cmps in enumerate(current_comparisons):
            total_comparisons[i].append(cmps)
        print(" ",r,"Done")
    for i,sortfunc in enumerate(sortingfunctions):
        confidence_boxplot(total_comparisons[i],R,col = colormap(sortfunc), label = sortfunc.__name__, linest=linestylemap(sortfunc))
    return total_comparisons

def confidence_timvstopo_varyElems(nrange,runs,datagenerator,sortingfunctions,reps=100):
    N = list(nrange)
    total_comparisons = [[] for _ in range(len(sortingfunctions))]
    print("Starting elems for",datagenerator.__name__)
    for n in N:
        current_comparisons = [[] for _ in range(len(sortingfunctions))]
        for _ in range(100):
            lst = lst = [Value(y) for y in datagenerator(n,runs)]
            for i,sortfunc in enumerate(sortingfunctions):
                Value.reset_count() #some data generators sort things to build runs
                sortfunc(lst)
                current_comparisons[i].append(Value.comparisons)
        for i,cmps in enumerate(current_comparisons):
            total_comparisons[i].append(cmps)
        print(" ",n,"Done")
    for i,sortfunc in enumerate(sortingfunctions):
        confidence_boxplot(total_comparisons[i],N,col = colormap(sortfunc),label = sortfunc.__name__, linest=linestylemap(sortfunc))
    return total_comparisons

from DataGenerators import all_data_distributions,set_name, visualize_datagen
from PersiSort import PersiSort
from TimSort import TimSort

@set_name("Python v 3.11.2")
def PythonSort(lst):
    return sorted(lst)

from PowerSort import powersort
powersort.__name__ = "PowerSort+Finger"

def sorting_functions():
    return [
        TimSort,
        PythonSort,
        PersiSort,
        powersort
    ]

def colormap(x):
    """
    https://davidmathlogic.com/colorblind/
    """
    cmap = { 
        PersiSort : "#FE6100",
        TimSort : "#785EF0",
        PythonSort : "#DC267F",
        powersort : "#648FFF"
    }
    return cmap[x]
def linestylemap(x):
    lmap = { 
        PersiSort : "solid",
        TimSort : "dotted",
        PythonSort : "dashed",
        powersort : "dashdot"
    }
    return lmap[x]
def randomized_sort_func(x):
    rmap = {
        PersiSort : False,
        TimSort : False,
        PythonSort : False,
        powersort : False,
        sorted : False,
    }
    rmap.setdefault(False)
    return rmap[x]

from DataGenerators import overlapping_staircase
def overlapping_staircase_experiment(n,r,sortingfunctions,Omax = 60):
    O = list(range(1,Omax))
    total_comparisons = [[] for _ in range(len(sortingfunctions))]
    print("Starting overlapping staircase experiment")
    for o in O:
        current_comparisons = [[] for _ in range(len(sortingfunctions))]
        reps = 1
        for _ in range(100):
            lst = lst = [Value(y) for y in overlapping_staircase(n,r,o)]
            for i,sortfunc in enumerate(sortingfunctions):
                Value.reset_count() #some data generators sort things to build runs
                _ = sortfunc(lst)
                current_comparisons[i].append(Value.comparisons)
        for i,cmps in enumerate(current_comparisons):
            total_comparisons[i].append(cmps)
        print(" ",o,"Done")
    for i,sortfunc in enumerate(sortingfunctions):
        confidence_boxplot(total_comparisons[i],O,col = colormap(sortfunc), label = sortfunc.__name__, linest=linestylemap(sortfunc))

def overlapping_staircase_paper_version(rows=1,row=0):
    n = 20000
    r = 300
    Omax = n//r
    #plt.subplots(1,2,width_ratios=[1,2])

    plt.subplot(rows,3,1+3*row)
    plt.title(f"Distribution Visualization")
    visualize_datagen(lambda x,y: overlapping_staircase(x,y,4),100,8)
    plt.axis("off")
    
    plt.subplot(rows,3,2+3*row)
    plt.title("Varying overlap")
    overlapping_staircase_experiment(n,r,sorting_functions(),Omax = Omax)
    plt.legend()
    #plt.axis("off")
    
    plt.subplot(rows,3,3+3*row)
    plt.title("Varying overlap zoom")
    funcs = [f for f in sorting_functions() if f != PythonSort ]
    overlapping_staircase_experiment(n,r,funcs,Omax = Omax//2)
    #plt.legend()
    #plt.axis("off")
    
    if row == 0:
        figure = plt.gcf() # get current figure
        figure.set_size_inches(10,5)
        figure.tight_layout()

    #plt.suptitle(overlapping_staircase.__name__)
    plt.savefig(f"plots2/Overlapping_Staircase_{n=}_{r=}",dpi=600)
    plt.show()


def experiments(datagens,rows=1,row=0,SortingFunctions = sorting_functions(),folder="plots"):
    Nmax = 3000
    Nmin = 150
    Nstep = 100
    Rmax = 750
    Rmin = 10
    Rstep = 25
    singleplot = 0
    if row > 0:
        singleplot = 1
    s = len(datagens)
    start = time()
    start_ = time()
    for i,datadist in enumerate(datagens):
        if fixed_runs_possible(datadist):
            numcols = 3
        else:
            numcols = 2
        plt.subplot(rows,numcols,1+singleplot*(row+i)*3)
        plt.ylabel(datadist.__name__)
        plt.title(f"Distribution Visualization")
        data = visualize_datagen(datadist,100,9)
        plt.axis('off')
        plt.subplot(rows,numcols,2+singleplot*(row+i)*3)
        nrange = range(Nmin,Nmax+1,Nstep)
        data1 = confidence_timvstopo_varyElems(nrange,50,datadist,SortingFunctions)
        plt.xlabel("Number of elements")
        plt.ylabel("Comparisons")
        plt.title("Varying elements")
        data2 = []
        Rrange = []
        if fixed_runs_possible(datadist):
            plt.subplot(rows,numcols,3+singleplot*(row+i)*3)
            Rrange = range(Rmin,Rmax,Rstep)
            data2 = confidence_timvstopo_varyRuns(Nmax,Rrange,datadist,SortingFunctions)
            plt.title("Varying runs")
            plt.xlabel("Number of runs")
            plt.ylabel("Comparisons")
            plt.suptitle(datadist.__name__)
            print(f" {datadist.__name__} completed in",round((time()-start)/60,2),"minutes")
        
        figure = plt.gcf() # get current figure
        figure.tight_layout()
        figure.set_size_inches(10,5)
        
        start = time()
        if singleplot == 0:
            plt.savefig(f"{folder}/{datadist.__name__}_,{list(f.__name__.replace('.',',') for f in SortingFunctions)},{Nmax=},{Rmax=}",dpi=600)
            plt.show()
            plt.clf()
    print("Experiments completed in",round((time()-start_)/360,2),"hours")

from PersiSort import persistencepair_levels
def draw_red_box(p1,p2,col="r"):
    x1,y1 = p1
    x2,y2 = p2
    min_x, max_x = min([x1,x2]), max([x1,x2])
    min_y, max_y = min([y1,y2]), max([y1,y2])
    plt.plot([min_x,min_x,max_x,max_x,min_x],[min_y,max_y,max_y,min_y,min_y],"-",color =col,linewidth = 2)
def draw_red_box_lst(lst,p1,p2,col="r"):
    x1,y1 = p1
    x2,y2 = p2
    min_x, max_x = min([x1,x2]), max([x1,x2])
    min_y, max_y = min(min([y1,y2]),min(lst[min_x:max_x])),max(max([y1,y2]),max(lst[min_x:max_x]))
    plt.plot([min_x,min_x,max_x,max_x,min_x],[min_y,max_y,max_y,min_y,min_y],"-",color =col,linewidth = 2)

def visualize_datagen_perspairs(data):
    colors = ["orange","green","purple","black","red"]
    pairs = persistencepair_levels(data)
    plt.plot(data,".-") #remove this for experiments
    i=0
    for level in pairs:
        for (x1,x2) in level:
            draw_red_box_lst(data,(x1,data[x1]),(x2,data[x2]),col = colors[i%len(colors)])
        i+=1

def box_data_helper(data,name):
    visualize_datagen_perspairs(data)
    plt.axis("off")
    plt.savefig(f"box_plots/{name}_boxes",dpi=600)
    plt.clf()

def box_data():
    box_data_helper(staircase(100,9),"staircase")
    box_data_helper(uniform_data(20,9),"uniform")
    box_data_helper(isolated_pairs(45,6),"isolated_pairs")
    box_data_helper(super_nesting(45,9),"super_nesting")
    box_data_helper(TimSort_nemesis(30,0),"timsort_nemesis")
    box_data_helper(ultra_nesting(20,0),"ultra_nesting")

def check_parity(a,b):
    if a <= b:
        return 1
    else:
        return -1

def rundecomp(X):
    runs = []
    i = 2
    n = len(X)
    current_run = [X[0],X[1]]
    current_parity = check_parity(X[0],X[1])
    while i < n:
        next_parity = check_parity(X[i-1],X[i])
        if current_parity == next_parity:
            current_run.append(X[i])
            i += 1
        elif i+1 == n:
            runs.append(current_run)
            last_run = [X[i]]
            runs.append(last_run)
            return runs
        else:
            runs.append(current_run)
            current_run = [X[i],X[i+1]]
            current_parity = check_parity(X[i],X[i+1])
            i += 2
    if current_run in runs:
        return runs
    else:
        return runs+[current_run]

if __name__ == "__main__":
    overlapping_staircase_paper_version()
    experiments(all_data_distributions())
    exit()