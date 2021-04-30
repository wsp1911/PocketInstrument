import numpy as np
from numpy import sin, cos, exp, pi, e
import wave
import sys, os, glob
import scipy
from scipy import signal


def SineWave(fs, chunk, f, vpp, offset, phi):
    period = int(np.ceil(f * chunk / fs))
    x = np.arange(0, period / f, 1 / fs)
    y = offset + vpp / 2 * sin(2 * pi * f * x + phi / 180 * pi)
    return round(fs / f), y


def SquareWave(fs, chunk, f, vpp, duty, offset, phi):
    period = int(np.ceil(f * chunk / fs))
    N = round(fs / f)
    x = np.arange(period * N)
    y = offset + vpp * (x % N < duty * N) - vpp / 2
    N_phi = int(phi / 360 * N)
    return N, np.r_[y[N_phi:], y[:N_phi]]


def SawtoothWave(fs, chunk, f, vpp, offset, phi):
    period = int(np.ceil(f * chunk / fs))
    N = round(fs / f)
    y = offset + np.linspace(-vpp / 2, vpp / 2, N)
    N_phi = int(phi / 360 * N)
    return N, np.tile(np.r_[y[N_phi:], y[:N_phi]], period)


def TriangleWave(fs, chunk, f, vpp, width, offset, phi):
    period = int(np.ceil(f * chunk / fs))
    N = round(fs / f)
    N1 = round(N * width)
    y = (
        offset
        + np.r_[
            np.linspace(-vpp / 2, vpp / 2, N1),
            np.linspace(vpp / 2, -vpp / 2, N - N1 + 1)[1:],
        ]
    )
    N_phi = int(phi / 360 * N)
    return N, np.tile(np.r_[y[N_phi:], y[:N_phi]], period)


def DC(chunk, vpp):
    return chunk, vpp * np.ones(chunk)


def from_exp(fs, chunk, factor, s: str):
    try:
        id1 = s.find(",")
        t1 = 0 if id1 == -1 else eval(s[:id1])
        id2 = s.find(";")
        t2 = 1 if id2 == -1 else eval(s[id1 + 1 : id2])
        t = np.arange(t1, t2, 1 / fs)
        y = factor * eval(s[id2 + 1 :])
        N = len(y)
        period = int(np.ceil(chunk / N))
        return N, np.tile(y, period)
    except Exception:
        return False


def from_file(fs, chunk, s: str):
    try:
        if s[1] != ":":
            s = sys.path[0] + "\\" + s
        if s[-4:].lower() == ".wav":
            f = wave.open(s, "rb")
            params = f.getparams()
            nchannels, svppwidth, framerate, nframes = params[:4]
            strData = f.readframes(nframes)
            waveData = np.frombuffer(strData, dtype=np.int16)[::nchannels]
            waveData = waveData / 32768
            if framerate != fs:
                waveData = signal.resvpple_poly(waveData, fs, framerate)
            N = len(waveData)
            period = int(np.ceil(chunk / N))
            return N, np.tile(waveData, period)
        else:
            if s[-4:].lower() == ".mat":
                data = scipy.io.loadmat(s)
                data = data[data.keys()[0]].flatten()
            elif s[-4:].lower() == ".npy":
                data = np.load(s)
            N = len(data)
            period = int(np.ceil(chunk / N))
            return N, np.tile(data, period)
    except Exception:
        return -1, np.zeros(chunk)


def getWave(
    wave_type, CHUNK, factor, fs, f, vpp, duty, offset, phi, expression, filename
):
    if wave_type == 0:
        return -1, np.zeros(CHUNK)
    elif wave_type == 1:
        return SineWave(fs, CHUNK, f, vpp * factor, offset, phi)
    elif wave_type == 2:
        return SquareWave(fs, CHUNK, f, vpp * factor, duty, offset, phi)
    elif wave_type == 3:
        return DC(CHUNK, vpp * factor)
    elif wave_type == 4:
        return TriangleWave(fs, CHUNK, f, vpp * factor, duty, offset, phi)
    elif wave_type == 5:
        return SawtoothWave(fs, CHUNK, f, vpp * factor, offset, phi)
    elif wave_type == 6:
        return from_exp(fs, CHUNK, factor, expression)
    elif wave_type == 7:
        return from_file(fs, CHUNK, filename)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fs = 96000
    f = 1000
    vpp = 1
    offset = 0
    phi = 0
    duty = 0.5
    CHUNK = 1024
    N, y1 = SineWave(fs, CHUNK, f, vpp, offset, phi)
    N, y2 = SquareWave(fs, CHUNK, f, vpp, duty, offset, phi)
    N, y5 = SawtoothWave(fs, CHUNK, f, vpp, offset, phi)
    N, y4 = TriangleWave(fs, CHUNK, f, vpp, duty, offset, phi)
    N, y3 = DC(CHUNK, vpp)
    N, y6 = from_exp(fs, CHUNK, 1.0, "0,1;np.sin(100*t)*np.exp(-t)")
    # y7 = from_file(CHUNK, fs, "fmt.wav")
    N, y7 = from_file(fs, CHUNK, "test.npy")
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
