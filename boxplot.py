from statistics import median
import matplotlib.pyplot as plt

def boxplot(lst):
    """
    Minimum (Q0 or 0th percentile): the lowest data point in the data set excluding any outliers
    Maximum (Q4 or 100th percentile): the highest data point in the data set excluding any outliers
    Median (Q2 or 50th percentile): the middle value in the data set
    First quartile (Q1 or 25th percentile): also known as the lower quartile qn(0.25), it is the median of the lower half of the dataset.
    Third quartile (Q3 or 75th percentile): also known as the upper quartile qn(0.75), it is the median of the upper half of the dataset.[7]
    """
    Q0 = min(lst)
    Q4 = max(lst)
    Q2 = median(lst)
    Q1 = median([x for x in lst if x <= Q2])
    Q3 = median([x for x in lst if x >= Q2])
    return Q0, Q1, Q2, Q3, Q4

def confidence_boxplot(lst,X,col,label,linest="-"):
    """
    L a matrix of reps
    X values
    repetitions to calculate average
    """
    mins, Q1, avgs, Q3, maxs = zip(*[boxplot(L) for L in lst])

    plt.plot(X,avgs,marker=".",color = col,label = label,linestyle = linest)
    plt.fill_between(X, mins, maxs, color = col, alpha=.1)
    plt.fill_between(X, Q1, Q3, color = col, alpha=.3)