# -*- coding: utf-8 -*-
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt5.QtCore import pyqtSlot
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import sys, time
from Ui_va import Ui_MainWindow

# import wave
from pyaudio import PyAudio, paInt16

# from scipy.io import wavfile

import threading

matplotlib.use("Qt5Agg")
# matplotlib.rcParams["figure.figsize"] = [10, 10]  # for square canvas

# matplotlib.rcParams["figure.subplot.left"] = 0.03
# matplotlib.rcParams["figure.subplot.bottom"] = 0.03
# matplotlib.rcParams["figure.subplot.right"] = 0.9
# matplotlib.rcParams["figure.subplot.top"] = 1

# matplotlib.rcParams["figure.subplot.left"] = 0
# matplotlib.rcParams["figure.subplot.bottom"] = 0
# matplotlib.rcParams["figure.subplot.right"] = 0.9
# matplotlib.rcParams["figure.subplot.top"] = 1

matplotlib.rcParams["figure.facecolor"] = "black"
matplotlib.rcParams["axes.facecolor"] = "black"
matplotlib.rcParams["axes.edgecolor"] = "gray"
matplotlib.rcParams["text.color"] = "white"
# normalized for 中文显示和负号
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
# matplotlib.rcParams["xtick.direction"] = "in"  # 将x周的刻度线方向设置向内
# matplotlib.rcParams["ytick.direction"] = "in"  # 将y轴的刻度方向设置向内

# EXIT = False


# class Myplot for plotting with matplotlib
class Myplot(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        # new figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        # 主窗口
        sig_pos = [0.02, 0.3, 0.85, 0.67]
        self.ax_sig = self.fig.add_axes(sig_pos)

        # 显示每格刻度
        sigU_H = 0.03
        sigU_pos = [0, 1 - sigU_H, 1, sigU_H]
        self.ax_sigU = self.fig.add_axes(sigU_pos)
        self.init_ax(self.ax_sigU)

        # 显示GND
        sigL_pos = [0, sig_pos[1], 0.02, sig_pos[3]]
        self.ax_sigL = self.fig.add_axes(sigL_pos)
        self.init_ax(self.ax_sigL)

        # 显示测量数据
        sigR_pos = [
            sig_pos[0] + sig_pos[2] + 0.005,
            sig_pos[1],
            1 - sig_pos[0] - sig_pos[2] - 0.005,
            sig_pos[3],
        ]
        self.ax_sigR = self.fig.add_axes(sigR_pos)
        self.init_ax(self.ax_sigR)

        # 副窗口，显示FFT
        self.ax_fft = self.fig.add_axes([0, 0.05, 1, 0.25])

        # 两通道颜色
        self.c = ["#ffff00", "#00ff00"]

        y = [0.05 * i for i in range(21)]
        self.fixed_text = {
            "1": self.ax_sigU.text(0, 0, "1", c=self.c[0], fontsize=20),
            "2": self.ax_sigU.text(0.3, 0, "2", c=self.c[1], fontsize=20),
            "X1": self.ax_sigR.text(0, y[13], "X1/ms", c="white", fontsize=20),
            "X2": self.ax_sigR.text(0, y[11], "X2/ms", c="white", fontsize=20),
            "Y1": self.ax_sigR.text(0, y[9], "Y1/V", c="white", fontsize=20),
            "Y2": self.ax_sigR.text(0, y[7], "Y2/V", c="white", fontsize=20),
            "dX": self.ax_sigR.text(0, y[5], r"$\Delta$X/ms", c="white", fontsize=20),
            "1/dX": self.ax_sigR.text(
                0, y[3], "1/" + r"$\Delta$X/Hz", c="white", fontsize=20
            ),
            "dY": self.ax_sigR.text(0, y[1], r"$\Delta$Y/V", c="white", fontsize=20),
        }

        self.data = {
            "1": self.ax_sigU.text(0.02, 0, "0", fontsize=20),
            "2": self.ax_sigU.text(0.32, 0, "0", fontsize=20),
            "t": self.ax_sigU.text(0.8, 0, "0", fontsize=20),
            "X1": self.ax_sigR.text(
                1, y[12], "0", c="white", fontsize=20, horizontalalignment="right"
            ),
            "X2": self.ax_sigR.text(
                1, y[10], "0", c="white", fontsize=20, horizontalalignment="right"
            ),
            "Y1": self.ax_sigR.text(
                1, y[8], "0", c="white", fontsize=20, horizontalalignment="right"
            ),
            "Y2": self.ax_sigR.text(
                1, y[6], "0", c="white", fontsize=20, horizontalalignment="right"
            ),
            "dX": self.ax_sigR.text(
                1, y[4], "0", c="white", fontsize=20, horizontalalignment="right"
            ),
            "1/dX": self.ax_sigR.text(
                1, y[2], "0", c="white", fontsize=20, horizontalalignment="right"
            ),
            "dY": self.ax_sigR.text(
                1, y[0], "0", c="white", fontsize=20, horizontalalignment="right"
            ),
        }

        for i in range(2, 20, 2):
            self.ax_sigR.axhline(y=y[i], c="gray")

        # initial figure
        self.compute_initial_figure()

        # size policy
        FigureCanvas.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        FigureCanvas.updateGeometry(self)

    def init_ax(self, ax):
        ax.set_xlim((0, 1))
        ax.set_ylim((0, 1))
        ax.set_xticks([])
        ax.set_yticks([])

    def compute_initial_figure(self):
        pass


# class for the application window
class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        self.setupUi(self)
        self.fig = Myplot(width=5, height=5, dpi=100)

        # self.fig_ntb1 = NavigationToolbar(self.fig1, self)

        # add the static_fig in the Plot box
        self.gridlayout1 = QGridLayout(self.FigQGB)
        self.gridlayout1.addWidget(self.fig)
        # self.gridlayout1.addWidget(self.fig_ntb1)

        # self.CHUNK = 16384 // 2  # wav文件是由若干个CHUNK组成的，CHUNK我们就理解成数据包或者数据片段。
        self.CHUNK = 1024
        self.FORMAT = paInt16  # 表示我们使用量化位数 16位来进行录音
        self.CHANNELS = 2  # 代表的是声道，1是单声道，2是双声道。
        self.RATE = 44100  # 采样率 一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz,
        # 11.025kHz, 22.05kHz, 44.1kHz。
        self.SECTION = self.CHUNK // 16
        self.signal = [np.zeros(self.CHUNK), np.zeros(self.CHUNK)]
        self.factor = 5 * 3.247
        self.dispSignal = [np.zeros(self.SECTION), np.zeros(self.SECTION)]
        self.dispStart, self.dispLen = 0, self.SECTION
        self.T = np.arange(self.CHUNK) / self.RATE

        self.RUNNING = True
        self.CURSOR = False
        self.REFRESH = False
        self.RETRIG = False
        self.TRIGS, self.TRIGE = 0, 10
        self.MISS = False
        self.TRIGGERED = False

        self.CursorX[0].setParameters(0, self.T[self.dispLen - 1], 1000)
        self.CursorX[1].setParameters(0, self.T[self.dispLen - 1], 1000)
        self.CursorX[1].setValue(self.T[self.dispLen - 1])
        self.CursorY[1].setValue(10)

        self.connect()

    def connect(self):
        self.CursorX[0].valueChanged.connect(self.refreshFig)
        self.CursorX[1].valueChanged.connect(self.refreshFig)
        self.CursorY[0].valueChanged.connect(self.refreshFig)
        self.CursorY[1].valueChanged.connect(self.refreshFig)
        self.ZoomInput[0].valueChanged.connect(self.refreshFig)
        self.ZoomInput[1].valueChanged.connect(self.refreshFig)
        self.OffsetInput[0].valueChanged.connect(self.refreshFig)
        self.OffsetInput[1].valueChanged.connect(self.refreshFig)
        self.MeasChanMultiple.currentIndexChanged.connect(self.refreshFig)

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

    @pyqtSlot()
    def on_CursorButton_clicked(self):
        if self.CURSOR:
            self.CursorButton.setText("Off")
        else:
            self.CursorButton.setText("On")
        self.CURSOR = not self.CURSOR

        self.refreshFig()

    @pyqtSlot(int)
    def on_Trigger_valueChanged(self, val):
        self.TRIGE = self.TRIGS = time.perf_counter()

        self.refreshFig()

    @pyqtSlot(float)
    def on_tZoomInput_valueChanged(self, val):
        L = int(self.SECTION / self.tZoomInput.value())
        self.CursorX[0].setMaximum(self.T[L - 1])
        self.CursorX[1].setMaximum(self.T[L - 1])

        self.refreshFig()

    def plot_fig(self):
        self.fig.ax_sig.clear()

        if self.RUNNING:
            self.dispSignal[0] = (
                self.signal[0][self.dispStart : self.dispStart + self.dispLen]
                * self.ZoomInput[0].value()
                + self.OffsetInput[0].value()
            )
            self.dispSignal[1] = (
                self.signal[1][self.dispStart : self.dispStart + self.dispLen]
                * self.ZoomInput[1].value()
                + self.OffsetInput[1].value()
            )

        t_max = (
            self.T[self.dispSignal[0].size - 1]
            if self.RUNNING
            else self.T[int(self.SECTION / self.tZoomInput.value()) - 1]
        )
        t = self.T[: self.dispSignal[0].size] / t_max * 10

        self.fig.ax_sig.plot(
            t,
            self.dispSignal[0],
            c=self.fig.c[0],
        )
        self.fig.ax_sig.plot(
            t,
            self.dispSignal[1],
            c=self.fig.c[1],
        )

        # display trigger voltage
        if self.TRIGE - self.TRIGS < 10:
            self.TRIGE = time.perf_counter()
            tgv = self.Trigger.value()
            self.fig.ax_sig.axhline(y=tgv, ls="--", c="orange")

        self.fig.ax_sig.set_ylim((-10, 10))
        self.fig.ax_sig.set_xlim((0, 10))

        # display FFT
        if self.RUNNING:
            self.fig.ax_fft.clear()
            n_fft = int(self.fftN.value())
            cid = self.fftChanMultiple.currentIndex()
            s = self.signal[cid][self.dispStart : self.dispStart + self.dispLen]
            S = np.fft.fft(s, n=n_fft)
            S_log = np.log10(np.abs(S[: n_fft // 2]))
            f = np.linspace(0, self.RATE // 2, n_fft // 2)
            self.fig.ax_fft.plot(f, S_log, c="purple")
            y_lim = [np.log(0.01), np.ceil(np.max(S_log))]
            self.fig.ax_fft.set_ylim((y_lim[0], y_lim[1]))
            self.fig.ax_fft.set_xlim((0, self.RATE // 2))
            # self.fig.ax_fft.set_yticks(np.arange(y_lim[0], y_lim[1] + 1))
            self.fig.ax_fft.set_xticks(np.arange(0, self.RATE // 2, 1000))
            self.fig.ax_fft.tick_params(axis="x", color="white", labelcolor="white")

        # display GND
        self.fig.ax_sigL.clear()
        self.fig.ax_sigL.set_ylim((-10, 10))
        self.fig.ax_sigL.axhline(y=self.OffsetInput[0].value(), c=self.fig.c[0])
        self.fig.ax_sigL.axhline(y=self.OffsetInput[1].value(), c=self.fig.c[1])

        # display the span
        self.fig.data["t"].set_text(str(round(1000 * t_max / 10, 4)) + "ms/")
        self.fig.data["1"].set_text(str(2 / self.ZoomInput[0].value()) + "V/")
        self.fig.data["2"].set_text(str(2 / self.ZoomInput[1].value()) + "V/")

        X = [c.value() for c in self.CursorX]
        Y = [c.value() for c in self.CursorY]
        # plot cursors
        if self.CURSOR:
            self.fig.ax_sig.axhline(y=Y[0], ls="--", c="orange")
            self.fig.ax_sig.axhline(y=Y[1], ls="--", c="orange")
            self.fig.ax_sig.axvline(x=X[0] / t_max * 10, ls="--", c="orange")
            self.fig.ax_sig.axvline(x=X[1] / t_max * 10, ls="--", c="orange")

        cid = self.MeasChanMultiple.currentIndex()

        # display measured result
        X0 = X[0] * 1000
        X1 = X[1] * 1000
        Y0 = (Y[0] - self.OffsetInput[cid].value()) / self.ZoomInput[cid].value()
        Y1 = (Y[1] - self.OffsetInput[cid].value()) / self.ZoomInput[cid].value()
        digits = 3
        self.fig.data["X1"].set_text(str(round(X0, digits)))
        self.fig.data["X2"].set_text(str(round(X1, digits)))
        self.fig.data["dX"].set_text(str(round(X1 - X0, digits)))
        self.fig.data["1/dX"].set_text(str(round(1000 / abs(X1 - X0), digits)))
        self.fig.data["Y1"].set_text(str(round(Y0, digits)))
        self.fig.data["Y2"].set_text(str(round(Y1, digits)))
        self.fig.data["dY"].set_text(str(round(Y1 - Y0, digits)))

        # divide the x and y axis into 10 parts
        self.fig.ax_sig.xaxis.set_ticks(np.linspace(0, 10, 11))
        self.fig.ax_sig.yaxis.set_ticks(np.linspace(-10, 10, 11))
        # display the grid
        self.fig.ax_sig.grid(True, c="gray")

        self.fig.draw()

    def measure(self):
        pass

    def genDebugData(self):
        amp = 0.2
        freq = 100
        t = np.arange(0, 10, 1 / self.RATE)
        N = len(t)
        y0 = amp * np.sin(2 * np.pi * freq * t)
        y1 = amp * np.cos(2 * np.pi * freq * t)

        y = np.zeros(N * 2)

        for i in range(N):
            y[2 * i] = y0[i]
            y[2 * i + 1] = y1[i]

        return (y * 32768).astype(np.int16).tobytes()

    def trigger(self):
        if self.dispStart + self.dispLen >= self.CHUNK:
            return 0
        tgv = self.Trigger.value()
        chan = self.TriggerChanMultiple.currentIndex()
        slope = self.TriggerSlopeMultiple.currentIndex()
        y = (
            self.signal[chan][self.dispStart : self.dispStart + self.dispLen]
            * self.ZoomInput[chan].value()
            + self.OffsetInput[chan].value()
        )
        if slope == 0:
            for i in range(1, self.dispLen):
                if y[i] - tgv >= 0 and y[i - 1] - tgv < 0:
                    return i
        else:
            for i in range(1, self.dispLen):
                if y[i] - tgv <= 0 and y[i - 1] - tgv > 0:
                    return i
        return 0

    def display(self, filepath=None):
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
                # data = self.genDebugData()
                data = np.frombuffer(raw_data, dtype=np.int16) / 32768
                self.signal[0] = self.factor * data[::2]
                self.signal[1] = self.factor * data[1::2]
            if self.REFRESH:  # 暂停状态时保持画面更新
                self.plot_fig()
                self.REFRESH = False
            while self.RUNNING:
                pos = self.trigger()
                # pos = 0
                self.dispLen = int(self.SECTION / self.tZoomInput.value())
                if self.dispStart + pos + self.dispLen >= self.CHUNK:
                    self.dispStart = 0
                    break

                self.dispStart += pos
                self.plot_fig()
                self.dispStart += self.dispLen

        stream.stop_stream()
        stream.close()  # 关闭
        pa.terminate()  # 终结


if __name__ == "__main__":
    # run = False
    run = True
    if run:
        app = QApplication(sys.argv)
        win = AppWindow()

        # win.tZoomInput.setValue(win.tZoomInput.minimum())

        win.show()
        t1 = threading.Thread(target=win.display)
        t1.start()
        sys.exit(app.exec_())
    else:
        app = QApplication(sys.argv)
        win = AppWindow()

        data = win.genDebugData()
        win.byte2num(data, gain=20)

        plt.plot(win.signal[0])
        plt.plot(win.signal[1])
        plt.show()

        sys.exit(app.exec_())
