from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import time


def extend(x, idx, target_len):
    x_len = len(x)
    if target_len <= x_len:
        if idx + target_len <= x_len:
            return x[idx : idx + target_len]
        else:
            return np.r_[x[idx:], x[: target_len + idx - x_len]]


def concat_test(N):
    L = 10000
    a = np.arange(L)
    rand_n = np.random.randint(2, L - 2, N)

    t1 = time.perf_counter()
    for i in range(N):
        y = np.r_[a[rand_n[i] :], a[: rand_n[i]]]
    t1 = time.perf_counter() - t1
    print("concat :%f" % (1000 * t1 / N))

    t1 = time.perf_counter()
    for i in range(N):
        for j in range(L):
            y[j] = a[(rand_n[i] + j) % L]
    t1 = time.perf_counter() - t1

    print("assign:%f" % (1000 * t1 / N))


def np_max_speed_test(N):
    t = np.arange(0, 10, 0.001)
    y = np.sin(2 * np.pi * 100 * t)

    rand_n = np.random.randint(0, len(y), N)

    t1 = time.perf_counter()
    for i in range(N):
        pks = signal.find_peaks(y)
    t1 = time.perf_counter() - t1
    print("find peaks time:%f" % (1000 * t1 / N))

    t1 = time.perf_counter()
    for i in range(N):
        ma = np.max(y)
    t1 = time.perf_counter() - t1
    print("max time:%f" % (1000 * t1 / N))

    t1 = time.perf_counter()
    for i in range(N):
        yi = y[rand_n[i]]
    t1 = time.perf_counter() - t1
    print("random access time:%f" % (1000 * t1 / N))


def trigger():
    idx = 0
    CHUNK = 8192
    RATE = 96000
    t = np.arange(CHUNK) / RATE
    disp_len = CHUNK // 8
    offset, zoom = 0, 1
    tgv = 0.5
    slope = 1 - 2 * 1

    while True:

        y = np.sin(2 * np.pi * 1000 * t + 2 * np.pi * np.random.rand())

        y1 = -np.abs(y[1:-disp_len] + (offset - tgv) / zoom)

        pks = signal.find_peaks(y1)
        for i in pks[0]:
            if (y[i + 1] - y[i]) * slope > 0:
                idx = i
                break
        if abs(zoom * y[idx] + offset - tgv) > 0.01:
            plt.subplot(2, 1, 1)
            # plt.plot(y1)
            plt.plot(y)
            for i in pks[0]:
                plt.plot(i, y[i], "ro")
            plt.subplot(2, 1, 2)
            plt.plot(t[:disp_len], y[:disp_len])
            plt.plot(t[idx : idx + disp_len], y[idx : idx + disp_len])
            plt.show()


if __name__ == "__main__":
    # np_max_speed_test(100000)
    concat_test(100)
