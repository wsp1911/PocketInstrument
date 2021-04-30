import numpy as np
from numpy import sin, cos, exp, pi, e
import wave
import sys, os, glob
import scipy
from scipy import signal


def SineWave(fs, f, amp, offset, phi):
    x = np.arange(0, 1 / f, 1 / fs)
    y = offset + amp * sin(2 * pi * f * x + phi / 180 * pi)
    return y


def SquareWave(fs, f, amp, duty, offset, phi):
    N = round(fs / f)
    x = np.arange(N)
    y = offset + amp * (x < duty * N)
    return y


def SawtoothWave(fs, f, amp, offset, phi):
    N = round(fs / f)
    y = offset + (np.linspace(0, amp, N) - amp / 2)
    return y


def TriangleWave(fs, f, amp, width, offset, phi):
    N = round(fs / f)
    N1 = round(N * width)
    y = offset * np.ones(N)
    for i in range(1, N1):
        y[i] = y[i - 1] + amp / N1
    for i in range(N1, N):
        y[i] = y[i - 1] - amp / (N - N1)
    return y


def DC(N, amp):
    return amp * np.ones(N)


def from_exp(CHUNK, fs, factor, s: str):
    try:
        id1 = s.find(",")
        t1 = 0 if id1 == -1 else eval(s[:id1])
        id2 = s.find(";")
        t2 = 1 if id2 == -1 else eval(s[id1 + 1 : id2])
        t = np.arange(t1, t2, 1 / fs)
        return factor * eval(s[id2 + 1 :])
    except Exception:
        return False


def from_file(CHUNK, fs, s: str):
    try:
        if s[1] != ":":
            s = sys.path[0] + "\\" + s
        if s[-4:].lower() == ".wav":
            f = wave.open(s, "rb")
            params = f.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            strData = f.readframes(nframes)
            waveData = np.frombuffer(strData, dtype=np.int16)[::nchannels]
            waveData = waveData / 32768
            if framerate != fs:
                waveData = signal.resample_poly(waveData, fs, framerate)
            return waveData
        else:
            if s[-4:].lower() == ".mat":
                data = scipy.io.loadmat(s)
                data = data[data.keys()[0]].flatten()
            elif s[-4:].lower() == ".npy":
                data = np.load(s)
            return data
    except Exception:
        return False


def getWave(
    wave_type, CHUNK, factor, fs, f, amp, duty, offset, phi, expression, filename
):
    if wave_type == 0:
        return np.zeros(CHUNK)
    elif wave_type == 1:
        return SineWave(fs, f, amp * factor, offset, phi)
    elif wave_type == 2:
        return SquareWave(fs, f, amp * factor, duty, offset, phi)
    elif wave_type == 3:
        return DC(CHUNK, amp * factor)
    elif wave_type == 4:
        return TriangleWave(fs, f, amp * factor, duty, offset, phi)
    elif wave_type == 5:
        return SawtoothWave(fs, f, amp * factor, offset, phi)
    elif wave_type == 6:
        return from_exp(CHUNK, fs, factor, expression)
    elif wave_type == 7:
        return from_file(CHUNK, fs, filename)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fs = 44100
    f = 1000
    amp = 1
    offset = 0
    phi = 0
    duty = 0.5
    CHUNK = 1024
    y1 = SineWave(fs, f, amp, offset, phi)
    y2 = SquareWave(fs, f, amp, duty, offset, phi)
    y5 = SawtoothWave(fs, f, amp, offset, phi)
    y4 = TriangleWave(fs, f, amp, duty, offset, phi)
    y3 = DC(CHUNK, amp)
    y6 = from_exp(CHUNK, fs, "0,1;np.sin(100*t)*np.exp(-t)")
    # y7 = from_file(CHUNK, fs, "fmt.wav")
    y7 = from_file(CHUNK, fs, "test.npy")
    M, N = 7, 1
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
    plt.subplot(M, N, 6)
    plt.plot(y6)
    plt.subplot(M, N, 7)
    plt.plot(y7)
    plt.show()
