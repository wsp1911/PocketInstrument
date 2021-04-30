import numpy as np
import matplotlib.pyplot as plt
import time


def trigger(y):
    idx = 0

    tgv = 0
    slope = 1 - 2 * 0

    for i in range(1, len(y)):
        if (y[i] - tgv) * slope >= 0 and (y[i - 1] - tgv) * slope < 0:
            idx = i
            break
    if len(y) - idx < len(y):
        idx = 0
    return idx


RATE = 44100
CHUNK = 2048
t = np.arange(0, CHUNK) / RATE
y = np.sin(2 * np.pi * 100 * t + 1)

trigger(y)
