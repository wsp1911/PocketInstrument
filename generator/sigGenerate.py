import numpy as np


def SineWave(fs, f, amp, offset, phi):
    x = np.arange(0, 1 / f, 1 / fs)
    y = offset + amp * np.sin(2 * np.pi * f * x + phi / 180 * np.pi)
    return y


def SquareWave(fs, f, amp, duty, offset, phi):
    N = round(fs / f)
    x = np.arange(N)
    y = offset + amp * (x < duty * N)
    # y = np.tile(y, 10).astype(np.float32)
    return y


def SawtoothWave(fs, f, amp, offset, phi):
    N = round(fs / f)
    y = offset + (np.linspace(0, amp, N) - amp / 2)
    # y = np.tile(y, 10)
    return y


def TriangleWave(fs, f, amp, width, offset, phi):
    N = round(fs / f)
    N1 = round(N * width)
    # y = offset + np.r_[np.linspace(0, amp, N1), np.linspace(0, amp, N - N1)[::-1]]
    y = offset * np.ones(N)
    for i in range(1, N1):
        y[i] = y[i - 1] + amp / N1
    for i in range(N1, N):
        y[i] = y[i - 1] - amp / (N - N1)
    # return np.r_[y[0], np.tile(y[1:], 10)]
    return y


def DC(amp):
    return amp * np.ones(100)


def getWave(wave_type, fs, f, amp, duty, offset, phi):
    if wave_type == 0:
        return 0
    elif wave_type == 1:
        return SineWave(fs, f, amp, offset, phi)
    elif wave_type == 2:
        return SquareWave(fs, f, amp, duty, offset, phi)
    elif wave_type == 3:
        return DC(amp)
    elif wave_type == 4:
        return TriangleWave(fs, f, amp, duty, offset, phi)
    elif wave_type == 5:
        return SawtoothWave(fs, f, amp, offset, phi)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fs = 44100
    f = 1000
    amp = 1
    offset = 0
    phi = 0
    dutyRatio = 0.5
    y1 = genSineWave(fs, f, amp, phi, offset)
    y2 = genSquareWave(fs, f, amp, dutyRatio, offset)
    y3 = genSawtoothWave(fs, f, amp, offset)
    y4 = genTriangleWave(fs, f, amp, dutyRatio, offset)
    y5 = genDC(amp)
    M, N = 5, 1
    plt.subplot(M, N, 1)
    plt.plot(y1)
    plt.subplot(M, N, 2)
    plt.plot(y2)
    plt.subplot(M, N, 3)
    plt.plot(y3)
    plt.subplot(M, N, 4)
    plt.plot(y4)
    plt.subplot(M, N, 5)
    plt.plot(y5)
    plt.show()
