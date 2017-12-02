import matplotlib.pyplot as plt
import numpy as np

def CDF(array, bins):
    n, bins, patches = plt.hist(array, bins, normed=True, cumulative=1, histtype='step')
    x = list(bins)
    y = list(n)
    y[0] = 0
    y.append(1)
    return [x, y]

def CCDF(array, bins):
    n, bins, patches = plt.hist(array, bins, normed=True, cumulative=-1, histtype='step')
    x = list(bins)
    y = list(n)
    y.append(0)
    return [x, y]

def StatLabel_(array):
    label = '(min=%d, max=%d, median=%.1f, mean=%.1f, std=%.1f)'%\
        (min(array), max(array), np.median(array), np.mean(array), np.std(array))
    return label

def StatLabel(array):
    label = 'min=%d, max=%d\nmedian=%d, mean=%.1f'%\
        (min(array), max(array), np.median(array), np.mean(array))
    return label

def histPlot(x, bins, xlabel, ylabel):
    plt.hist(x, bins)
    plt.xlabel(xlabel+' (median = %.1f, mean = %.1f)'%(median(x), mean(x)))
    plt.ylabel(ylabel)
    plt.show()
