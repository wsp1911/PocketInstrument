# -*- coding: utf-8 -*-
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt5.QtCore import pyqtSlot
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, sin, cos
import sys, time
from Ui_va import Ui_MainWindow

import wave
from pyaudio import PyAudio, paInt16

from scipy.io import savemat

import threading

matplotlib.use("Qt5Agg")

matplotlib.rcParams["figure.facecolor"] = "black"
matplotlib.rcParams["axes.facecolor"] = "black"
matplotlib.rcParams["axes.edgecolor"] = "gray"
matplotlib.rcParams["text.color"] = "white"
# normalized for 中文显示和负号
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False
# matplotlib.rcParams["xtick.direction"] = "in"  # 将x周的刻度线方向设置向内
# matplotlib.rcParams["ytick.direction"] = "in"  # 将y轴的刻度方向设置向内


# class for the application window
class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        self.setupUi(self)

        self.CHUNK = 1024 * 8
        self.FORMAT = paInt16  # 表示我们使用量化位数 16位来进行录音
        self.CHANNELS = 2  # 代表的是声道，1是单声道，2是双声道。
        self.RATE = 44100  # 采样率 一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz,
        # 11.025kHz, 22.05kHz, 44.1kHz。
        self.SECTION = self.CHUNK // 16
        self.raw_data = 0
        self.signal = [np.zeros(self.CHUNK), np.zeros(self.CHUNK)]
        self.factor = 5 * 3.247
        self.dispSignal = [np.zeros(self.SECTION), np.zeros(self.SECTION)]
        self.dispStart, self.dispLen = 0, self.SECTION
        self.T = np.arange(self.CHUNK) / self.RATE

        self.RUNNING = True
        self.REFRESH = False
        self.TRIGS, self.TRIGE = 0, 10
        self.SAVEPIC, self.SAVEDATA, self.RECORD = False, False, False

        self.pa = PyAudio()
        self.stream = self.pa.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
        )

        self.CursorX[0].setParameters(0, 1, self.CHUNK)
        self.CursorX[1].setParameters(0, 1, self.CHUNK)
        self.CursorX[1].setValue(1)
        self.CursorY[0].setParameters(-10, 10, 2000)
        self.CursorY[1].setParameters(-10, 10, 2000)
        self.CursorY[0].setValue(-10)
        self.CursorY[1].setValue(10)
        self.Trigger.setParameters(-10, 10, 2000)
        self.Trigger.setValue(0)

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
        self.CursorSource.currentIndexChanged.connect(self.refreshFig)
        self.tZoomInput.valueChanged.connect(self.refreshFig)

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
        self.RunButton.setFont(QtGui.QFont("宋体", self.font_size))
        self.RUNNING = not self.RUNNING

    @pyqtSlot(int)
    def on_Trigger_valueChanged(self, val):
        self.TRIGE = self.TRIGS = time.perf_counter()
        self.refreshFig()

    @pyqtSlot()
    def on_PicSaveButton_clicked(self):
        self.SAVEPIC = True

    def save_pic(self):
        filename = self.PicFileInput.text() + self.PicFormat.currentText()
        self.fig.fig.savefig(filename)
        self.SAVEPIC = False

    @pyqtSlot()
    def on_DataSaveButton_clicked(self):
        self.SAVEDATA = True

    def save_data(self):
        filename = self.DataFileInput.text()
        format_id = self.DataFormat.currentIndex()
        if format_id == 0:
            np.save(filename + ".npy", self.signal)
        elif format_id == 1:
            savemat(
                filename + ".mat",
                {"signal_0": self.signal[0], "signal_1": self.signal[1]},
            )
        elif format_id == 2:
            wf = wave.open(filename + ".wav", "wb")
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.pa.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(self.raw_data)
            wf.close()
        self.SAVEDATA = False

    @pyqtSlot()
    def on_RecordButton_clicked(self):
        self.RECORD = not self.RECORD

    def record(self):
        filename = self.RecordFileInput.text()
        format_id = self.RecordFormat.currentIndex()
        frames, cnt = [], 0

        self.RecordButton.setText("结束录音")
        # record 10 minutes at most
        while self.RECORD and cnt * self.CHUNK / self.RATE < 600:
            frames.append(self.stream.read(self.CHUNK))

        data_bytes = b"".join(frames)

        if format_id == 2:
            wf = wave.open(filename + ".wav", "wb")
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.pa.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(data_bytes)
            wf.close()
            self.RecordButton.setText("开始录音")
            return

        data = np.frombuffer(data_bytes, dtype=np.int16) / 32768
        signal_0 = self.factor * data[::2]
        signal_1 = self.factor * data[1::2]

        if format_id == 0:
            np.save(filename + ".npy", [signal_0, signal_1])
        elif format_id == 1:
            savemat(
                filename + ".mat",
                {"signal_0": self.signal_0, "signal_1": signal_1},
            )
        self.RecordButton.setText("开始录音")

    def plot_fig(self):
        display_mode = self.ModeSelect.currentIndex()

        # update data
        if self.RUNNING:
            self.dispSignal[0] = self.signal[0][
                self.dispStart : self.dispStart + self.dispLen
            ]
            self.dispSignal[1] = self.signal[1][
                self.dispStart : self.dispStart + self.dispLen
            ]
        # get t-axis data
        t_max = (
            self.T[self.dispSignal[0].size - 1]
            if self.RUNNING
            else self.T[int(self.SECTION / self.tZoomInput.value()) - 1]
        )
        t = self.T[: self.dispSignal[0].size] / t_max

        # main window
        if display_mode == 0:  # plot signal
            self.fig.ax.clear()
            self.fig.ax.plot(
                t,
                self.dispSignal[0] * self.ZoomInput[0].value()
                + self.OffsetInput[0].value(),
                c=self.fig.c[0],
            )
            self.fig.ax.plot(
                t,
                self.dispSignal[1] * self.ZoomInput[1].value()
                + self.OffsetInput[1].value(),
                c=self.fig.c[1],
            )
            # display trigger voltage
            if self.TRIGE - self.TRIGS < 10:
                self.TRIGE = time.perf_counter()
                tgv = self.Trigger.value()
                self.fig.ax.axhline(y=tgv, ls="--", c="orange")
            self.fig.ax.axis("auto")  # axis_equal后，set_xlim会无效
            self.fig.ax.set_ylim((-10, 10))
            self.fig.ax.set_xlim((0, 1))
            # divide the x and y axis into 10 parts
            self.fig.ax.xaxis.set_ticks(np.linspace(0, 1, 11))
            self.fig.ax.yaxis.set_ticks(np.linspace(-10, 10, 11))
            # display the grid
            self.fig.ax.grid(True, c="gray")
            # GND
            self.fig.ax_left.clear()
            self.fig.ax_left.set_ylim((-10, 10))
            self.fig.ax_left.axhline(y=self.OffsetInput[0].value(), c=self.fig.c[0])
            self.fig.ax_left.axhline(y=self.OffsetInput[1].value(), c=self.fig.c[1])
        elif display_mode == 1:  # XY plot
            self.fig.ax.clear()
            self.fig.ax.plot(
                self.dispSignal[0] * self.ZoomInput[0].value()
                + self.OffsetInput[0].value(),
                self.dispSignal[1] * self.ZoomInput[1].value()
                + self.OffsetInput[1].value(),
                c="purple",
            )
            self.fig.ax.axis("equal")

        # display the span
        self.fig.data["t"].set_text(str(round(1000 * t_max / 10, 4)) + "ms/")
        self.fig.data["1"].set_text(str(2 / self.ZoomInput[0].value()) + "V/")
        self.fig.data["2"].set_text(str(2 / self.ZoomInput[1].value()) + "V/")

        X = [c.value() for c in self.CursorX]
        Y = [c.value() for c in self.CursorY]
        # plot cursors
        if display_mode == 0:
            self.fig.ax.axhline(y=Y[0], ls="--", c="orange")
            self.fig.ax.axhline(y=Y[1], ls="--", c="orange")
            self.fig.ax.axvline(x=X[0], ls="--", c="orange")
            self.fig.ax.axvline(x=X[1], ls="--", c="orange")

            cid = self.CursorSource.currentIndex()

            # display measured result
            X0 = X[0] * t_max * 1000
            X1 = X[1] * t_max * 1000
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

        self.fig.draw()

        if self.SAVEPIC:
            self.save_pic()

        if self.SAVEDATA:
            self.save_data()

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

    def trigger(self):
        if self.dispStart + self.dispLen >= self.CHUNK:
            return 0
        tgv = self.Trigger.value()
        chan = self.TriggerSource.currentIndex()
        slope = self.TriggerSlopeSelect.currentIndex()
        y = (
            self.signal[chan][self.dispStart : self.dispStart + self.dispLen]
            * self.ZoomInput[chan].value()
            + self.OffsetInput[chan].value()
        )
        if slope == 0:
            for i in range(1, self.dispLen):
                if y[i] >= tgv and y[i - 1] < tgv:
                    return i
        else:
            for i in range(1, self.dispLen):
                if y[i] <= tgv and y[i - 1] > tgv:
                    return i
        return 0

    def run(self, filepath=None):
        while True:
            if self.RUNNING:
                if self.RECORD:
                    self.record()
                self.raw_data = self.stream.read(self.CHUNK)  # 读取chunk个字节 保存到data中
                # raw_data = self.genDebugData()
                data = np.frombuffer(self.raw_data, dtype=np.int16) / 32768
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

        self.stream.stop_stream()
        self.stream.close()  # 关闭
        self.pa.terminate()  # 终结


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    t1 = threading.Thread(target=win.run)
    t1.start()
    sys.exit(app.exec_())
