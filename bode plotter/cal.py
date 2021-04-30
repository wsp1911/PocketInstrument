import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# 0 for standard signal; 1 for response signal


def get_chunk(f, RATE):
    if f == 0:
        return 1024
    N = int(RATE / f)
    chunk = 2 ** int(np.log2(N * 6) + 1)
    return max(chunk, 1024)


def split_signal(f, RATE, CHUNK, y0, y1, height=0.01, connect=False):

    if f == 0:
        return 1, y0[-CHUNK:], y1[-CHUNK:]

    N = int(RATE / f)
    pks = signal.find_peaks(-y0, height=height, distance=N * 0.9)

    # plt.figure()
    # plt.plot(y0)
    # plt.plot(y1)
    # for i in pks[0]:
    #     plt.plot(i, y0[i], "o", markersize=2)
    # plt.show()

    # DC0 = np.mean(y0[: pks0[0][0] - N])
    # DC1 = np.mean(y1[: pks1[0][0] - N])

    # y0 -= DC0
    # y1 -= DC1

    end = pks[0][0] + CHUNK - 3 * N // 4

    for i in range(len(pks[0])):
        if pks[0][i] >= end:
            break

    return i - 1, y0[pks[0][0] : pks[0][i - 1]], y1[pks[0][0] : pks[0][i - 1]]


def cal_response(f, dt, N, y0, y1):

    if f == 0:
        return np.mean(y1) / np.mean(y0), 0

    t = np.linspace(0, N / f, len(y0))
    s0 = np.sin(2 * np.pi * f * t)
    s1 = np.cos(2 * np.pi * f * t)

    # plt.figure()
    # plt.plot(y0)
    # plt.plot(y1)
    # plt.plot(s0)
    # plt.plot(s1)
    # plt.show()

    Integral = [
        [np.sum(y0 * s0 * dt) * 2 * f / N, np.sum(y0 * s1 * dt) * 2 * f / N],
        [np.sum(y1 * s0 * dt) * 2 * f / N, np.sum(y1 * s1 * dt) * 2 * f / N],
    ]

    A0 = np.sqrt(Integral[0][0] ** 2 + Integral[0][1] ** 2)
    A1 = np.sqrt(Integral[1][0] ** 2 + Integral[1][1] ** 2)

    phi0 = np.arccos(Integral[0][0] / A0)
    phi1 = np.arccos(Integral[1][0] / A1)

    return A1 / A0, (phi0 - phi1) * 180 / np.pi


def get_response(f, RATE, CHUNK, y0, y1):
    N, y0, y1 = split_signal(f, RATE, CHUNK, y0, y1)
    A, phi = cal_response(f, 1 / RATE, N, y0, y1)
    return A, phi


if __name__ == "__main__":
    RATE = 44100
    f = 0
    CHUNK = get_chunk(f, RATE)

    y = np.load("y_%d.npy" % f)

    y0, y1 = y[1], y[0]

    N, yy0, yy1 = split_signal(f, RATE, CHUNK, y0, y1)

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(y0, linewidth=1)
    plt.plot(y1, linewidth=1)
    plt.subplot(2, 1, 2)
    plt.plot(yy0, linewidth=1)
    plt.plot(yy1, linewidth=1)

    plt.show()

    # A, phi = cal(y[1], y[0])
    # print(A, phi)
