# coding:utf-8
import matplotlib.pyplot as plt
import itertools
import numpy as np


def func(r=2):
    x = 0.2
    while True:
        yield r * x * (1 - x)
        x = r * x * (1 - x)


generation = 30
arr = np.linspace(2, 4, num=51)
for i in arr:
    y = list(itertools.islice(func(i), generation))
    x = list(range(generation))
    plt.title('R = {0}'.format(i))
    plt.plot(x, y, linewidth=4)
    plt.show()
