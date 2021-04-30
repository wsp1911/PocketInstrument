# -*- coding: utf-8 -*-
import matplotlib

# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSlot
import numpy as np
from numpy import pi, sin, cos
import sys, time
from Ui_sa import Ui_MainWindow

# import wave
from pyaudio import PyAudio, paInt16

# from scipy.io import wavfile

import threading

matplotlib.use("Qt5Agg")

matplotlib.rcParams["figure.facecolor"] = "black"
matplotlib.rcParams["axes.facecolor"] = "black"
matplotlib.rcParams["axes.edgecolor"] = "gray"
matplotlib.rcParams["text.color"] = "white"
# normalized for 中文显示和负号
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

# class for the application window
class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        self.setupUi(self)

        self.CHUNK = 1024 * 2
        self.FORMAT = paInt16  # 表示我们使用量化位数 16位来进行录音
        self.CHANNELS = 2  # 代表的是声道，1是单声道，2是双声道。
        self.RATE = 44100  # 采样率 一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz,
        # 11.025kHz, 22.05kHz, 44.1kHz。
        self.signal = [np.zeros(self.CHUNK), np.zeros(self.CHUNK)]
        self.factor = 5 * 3.247
        self.fft_lim = [-20, 80]
        self.S_dB = 0

        self.RUNNING = True
        self.REFRESH = False

        self.CursorX[0].setParameters(0, 1, int(self.fftN.maximum() / 2))
        self.CursorX[1].setParameters(0, 1, int(self.fftN.maximum() / 2))
        self.CursorX[1].setValue(1)
        self.CursorY[0].setParameters(self.fft_lim[0], self.fft_lim[1], 1000)
        self.CursorY[1].setParameters(self.fft_lim[0], self.fft_lim[1], 1000)
        self.CursorY[1].setValue(self.fft_lim[1])

        self.connect()

    def connect(self):
        self.CursorX[0].valueChanged.connect(self.refreshFig)
        self.CursorX[1].valueChanged.connect(self.refreshFig)
        self.CursorY[0].valueChanged.connect(self.refreshFig)
        self.CursorY[1].valueChanged.connect(self.refreshFig)
        self.WinSelect.currentIndexChanged.connect(self.refreshFig)
        self.RangeInput[0].valueChanged.connect(self.refreshFig)
        self.RangeInput[1].valueChanged.connect(self.refreshFig)

    def refreshFig(self):
        if not self.RUNNING:
            self.REFRESH = True

    @pyqtSlot()
    def on_RunButton_clicked(self):
        if self.RUNNING:
            self.RunButton.setText("Run")
            self.RunButton.setStyleSheet("background-color: green;")
        else:
            self.RunButton.setText("Stop")
            self.RunButton.setStyleSheet("background-color: red;")
        self.RunButton.setFont(QtGui.QFont("宋体", 14))
        self.RUNNING = not self.RUNNING

    def plot_fig(self):
        nfft = int(self.fftN.value())
        f = np.linspace(0, self.RATE // 2, nfft // 2)
        f_range = [self.RangeInput[0].value(), self.RangeInput[1].value()]
        if f_range[0] >= f_range[1] - 1:
            f_range = [0, self.RATE // 2]
        f0, f1 = (
            self.CursorX[0].value() * (f_range[1] - f_range[0]) + f_range[0],
            self.CursorX[1].value() * (f_range[1] - f_range[0]) + f_range[0],
        )
        y0, y1 = self.CursorY[0].value(), self.CursorY[1].value()

        if self.RUNNING:
            S = np.fft.fft(self.signal[self.Source.currentIndex()], n=nfft)
            self.S_dB = 20 * np.log10(np.abs(S[: nfft // 2]))
        self.fig.ax.clear()
        self.fig.ax.plot(f, self.S_dB, c="purple")
        self.fig.ax.axvline(x=f0, ls="--", c="orange")
        self.fig.ax.axvline(x=f1, ls="--", c="orange")
        self.fig.ax.axhline(y=y0, ls="--", c="orange")
        self.fig.ax.axhline(y=y1, ls="--", c="orange")
        self.fig.ax.set_ylim((self.fft_lim[0], self.fft_lim[1]))
        self.fig.ax.set_xlim((f_range[0], f_range[1]))
        self.fig.ax.set_yticks(np.arange(self.fft_lim[0], self.fft_lim[1] + 1, 5))
        self.fig.ax.set_xticks(np.linspace(f_range[0], f_range[1], 20))
        self.fig.ax.tick_params(color="white", labelcolor="white")

        # fft measured result
        self.fig.data["f1"].set_text(str(round(f0, 2)))
        self.fig.data["f2"].set_text(str(round(f1, 2)))
        self.fig.data["Y1"].set_text(str(round(y0, 2)))
        self.fig.data["Y2"].set_text(str(round(y1, 2)))
        self.fig.data["df"].set_text(str(round(f1 - f0, 2)))
        self.fig.data["dY"].set_text(str(round(y1 - y0, 2)))

        self.fig.draw()

    def genDebugData(self):
        amp = 0.2
        freq = 1000
        t = np.arange(0, 1, 1 / self.RATE)
        N = len(t)
        # y0 = amp * sin(2 * pi * freq * t) + amp / 2 * sin(
        #     3 * 2 * pi * freq * t
        # )
        # y1 = amp * cos(2 * pi * freq * t) + amp / 2 * cos(
        #     5 * 2 * pi * freq * t
        # )
        # y0 = amp * sin(2 * pi * freq * t)
        # y1 = amp * cos(2 * pi * freq * t)

        # 心形线
        y0 = 16 * sin(2 * pi * freq * t) ** 3 / 32
        y1 = (
            13 * cos(2 * pi * freq * t)
            - 5 * cos(2 * 2 * pi * freq * t)
            - 2 * cos(3 * 2 * pi * freq * t)
            - cos(4 * 2 * pi * freq * t)
        ) / 32

        # 内旋轮
        # t = np.arange(0, 1, 1 / self.RATE)
        # N = len(t)
        # R, r, d = 1, 0.1, 0.9
        # y0 = (
        #     (R - r) * cos(2 * pi * freq * t) + d * cos((R - r) / r * 2 * pi * freq * t)
        # ) / 10
        # y1 = (
        #     (R - r) * sin(2 * pi * freq * t) + d * sin((R - r) / r * 2 * pi * freq * t)
        # ) / 10

        y = np.zeros(N * 2)

        for i in range(N):
            y[2 * i] = y0[i]
            y[2 * i + 1] = y1[i]

        return (y * 32768).astype(np.int16).tobytes()

    def run(self, filepath=None):
        pa = PyAudio()
        stream = pa.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )
        while True:
            if self.RUNNING:
                raw_data = stream.read(self.CHUNK)  # 读取chunk个字节 保存到data中
                # raw_data = self.genDebugData()
                data = np.frombuffer(raw_data, dtype=np.int16) / 32768
                self.signal[0] = self.factor * data[::2]
                self.signal[1] = self.factor * data[1::2]
                self.plot_fig()
            if self.REFRESH:  # 暂停状态时保持画面更新
                self.plot_fig()
                self.REFRESH = False

        stream.stop_stream()
        stream.close()  # 关闭
        pa.terminate()  # 终结


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    t1 = threading.Thread(target=win.run)
    t1.start()
    sys.exit(app.exec_())
