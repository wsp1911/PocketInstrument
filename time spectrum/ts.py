# -*- coding: utf-8 -*-
import matplotlib

# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSlot
import numpy as np
from numpy import pi, sin, cos
import sys, time
from pyaudio import PyAudio, paInt16
import threading

from Ui_ts import Ui_MainWindow


matplotlib.use("Qt5Agg")
# normalized for 中文显示和负号
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False


# class for the application window
class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        self.setupUi(self)

        self.CHUNK = 1024
        self.FORMAT = paInt16  # 表示我们使用量化位数 16位来进行录音
        self.CHANNELS = 2  # 代表的是声道，1是单声道，2是双声道。
        self.RATE = 44100  # 采样率 一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz,
        # 11.025kHz, 22.05kHz, 44.1kHz。
        self.signal = [np.zeros(self.CHUNK), np.zeros(self.CHUNK)]
        self.factor = 5 * 3.247

        self.RUNNING = True

        self.nframes, self.nfft = 500, self.CHUNK

        self.X, self.Y = (
            np.arange(self.nfft // 2),
            np.ones(self.nfft // 2),
        )
        self.cid = self.Source.currentIndex()
        self.frames_id = 0

        self.cnt = 0

        self.init_fig()

    @pyqtSlot(int)
    def on_Source_currentIndexChanged(self):
        self.frames_id = 0
        self.init_fig()

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

    @pyqtSlot()
    def on_SaveButton_clicked(self):
        self.fig.fig.savefig("test.png")

    def init_fig(self):
        self.fig.ax.clear()
        self.fig.ax.imshow(
            np.zeros((self.nframes, self.nfft // 2), dtype=np.uint8), origin="lower"
        )
        self.fig.ax.axis("auto")
        self.fig.ax.set_xticks(
            np.arange(0, self.nfft // 2, self.nfft * 1000 / self.RATE)
        )
        self.fig.ax.set_xticklabels(np.arange(0, self.RATE // 2, 1000))
        self.fig.draw()

    def plot_fig(self):
        S = np.fft.fft(self.signal[self.Source.currentIndex()], n=self.nfft)
        S_dB = 20 * np.log10(np.abs(S[: self.nfft // 2]))

        self.fig.ax.scatter(
            self.X, self.frames_id * self.Y, c=S_dB, vmin=-20, vmax=80, marker="_"
        )
        self.frames_id = (self.frames_id + 1) % self.nframes
        self.fig.ax.axis("auto")
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

        if self.cnt < 50:
            self.cnt += 1
        df = self.cnt * 100
        y0 = amp * sin(2 * pi * (freq + df) * t)
        y1 = amp * cos(2 * pi * (freq + df) * t)

        # 心形线
        # y0 = 16 * sin(2 * pi * freq * t) ** 3 / 32
        # y1 = (
        #     13 * cos(2 * pi * freq * t)
        #     - 5 * cos(2 * 2 * pi * freq * t)
        #     - 2 * cos(3 * 2 * pi * freq * t)
        #     - cos(4 * 2 * pi * freq * t)
        # ) / 32

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
