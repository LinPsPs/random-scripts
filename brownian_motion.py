import matplotlib.pyplot as plt
import numpy as np


def drawBMpath(t0, tn, n):
    step = (tn - t0) / n
    w = np.zeros(n)
    t = np.zeros(n)
    for i in range(1, n):
        eti = np.random.normal(0, 1)
        w[i] = w[i-1] + eti * np.sqrt(step)
        t[i] = t[i-1] + step
    plt.plot(t, w)
    plt.show()


drawBMpath(0, 1, 1000)


def areaBMpath(t0, tn, n):
    step = (tn - t0) / n
    w = np.zeros(n)
    cnt = 0
    for i in range(1, n):
        eti = np.random.normal(0, 1)
        w[i] = w[i-1] + eti * np.sqrt(step)
        cnt += w[i] * step
    return cnt / n


arr = [areaBMpath(0, 1, 1000) for _ in range(10 ** 5)]


plt.hist(arr)
plt.show()
print('Mean: ', np.mean(arr), 'std: ', np.std(arr))
