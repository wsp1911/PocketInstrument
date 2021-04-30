# -*- coding: utf-8 -*-
import matplotlib

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, sin, cos
import sys, time
from Ui_scope import Ui_MainWindow
from SignalGenerator import SignalGenerator
from sigGenerate import getWave
from multiprocessing import Process
from threading import Thread

# from SignalGenerator import SignalGenerator
# from BodePlotter import BodePlotter

import wave
from pyaudio import PyAudio, paInt16, paContinue

from scipy.io import savemat

import threading

matplotlib.use("Qt5Agg")

matplotlib.rcParams["figure.facecolor"] = "black"
matplotlib.rcParams["axes.facecolor"] = "black"
matplotlib.rcParams["axes.edgecolor"] = "gray"
matplotlib.rcParams["text.color"] = "white"
matplotlib.rcParams["xtick.color"] = "white"
matplotlib.rcParams["ytick.color"] = "white"
# normalized for 中文显示和负号
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False


class worker(QObject):
    def __init__(self, parent=None, win=None):
        super(worker, self).__init__(parent=parent)
        self.win = win

    def run(self):
        self.win.run()


class worker_plot(QObject):
    def __init__(self, parent=None, win=None):
        super(worker_plot, self).__init__(parent=parent)
        self.win = win

    def run(self):
        while self.win.RUNNING:
            self.win.plot_fig_t()
            self.win.plot_fig_f()


# class worker1(QObject):
#     def __init__(self,parent=None,win=None)

# class for the application window
class AppWindow(Ui_MainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)

        self.CHUNK = 8192
        self.FORMAT = paInt16  # 表示我们使用量化位数 16位来进行录音
        self.CHANNELS = 2  # 代表的是声道，1是单声道，2是双声道。
        self.RATE = 96000  # 采样率 一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz, 11.025kHz, 22.05kHz, 44.1kHz。
        self.rec_bytes = bytes()
        self.rec_y = [np.zeros(self.CHUNK), np.zeros(self.CHUNK)]
        self.input_gain = 10
        self.disp_sig = [0, 0]
        self.disp_len = self.CHUNK // 16
        self.disp_sig = [self.rec_y[0][: self.disp_len], self.rec_y[1][: self.disp_len]]
        self.T = np.arange(self.CHUNK) / self.RATE

        self.f_max = self.RATE // 2
        self.disp_FFT = [0, 0]

        self.TX, self.TY, self.FX, self.FY = [0, 1], [0, 1], [0, 1], [0, 1]

        self.RUNNING = False
        self.EXIT = False
        self.UPDATE = [False, False]
        self.TRIGT = time.perf_counter() - 5

        self.UPDATE_PLAYBYTES = False

        self.sg = SignalGenerator(parent=self, chunk=self.CHUNK, rate=self.RATE)

        self.worker = [worker(win=self), worker_plot(win=self)]
        self.threads = [QThread(), QThread()]

        self.worker[0].moveToThread(self.threads[0])
        self.worker[1].moveToThread(self.threads[1])

        # self.Bode_plotter = BodePlotter()

        self.tb_actions = self.toolbar.actions()

        self.tmp = time.perf_counter()

        self.connect()

    def calibrate(self):
        if self.RUNNING:
            self.statusbar.showMessage("先关闭示波器")
            return

    def open_generator(self):
        self.sg.show()

    # def open_Bode_plotter(self):
    #     self.Bode_plotter.show()

    def connect(self):
        self.tb_actions[0].triggered.connect(self.calibrate)
        self.tb_actions[1].triggered.connect(self.open_generator)
        # self.tb_actions[2].triggered.connect(self.open_Bode_plotter)

        self.threads[0].started.connect(self.worker[0].run)
        self.threads[1].started.connect(self.worker[1].run)

        self.Channel.currentIndexChanged.connect(self.update_fig)

        self.CursorTarget.currentIndexChanged.connect(self.update_by_cursor)
        self.CursorX[0].valueChanged.connect(self.update_by_cursor)
        self.CursorX[1].valueChanged.connect(self.update_by_cursor)
        self.CursorY[0].valueChanged.connect(self.update_by_cursor)
        self.CursorY[1].valueChanged.connect(self.update_by_cursor)

        self.Trigger[0].valueChanged.connect(self.update_trig_time)
        self.Trigger[1].valueChanged.connect(self.update_trig_time)

        self.CursorCB.stateChanged.connect(self.update_fig_t)
        self.MeasChan.currentIndexChanged.connect(self.update_fig_t)
        self.tYZoom[0].valueChanged.connect(self.update_fig_t)
        self.tYZoom[1].valueChanged.connect(self.update_fig_t)
        self.Offset[0].valueChanged.connect(self.update_fig_t)
        self.Offset[1].valueChanged.connect(self.update_fig_t)

        self.tZoom.valueChanged.connect(self.update_by_trigger)  # 显示长度改变后防止越界需要再触发
        self.Trigger[0].valueChanged.connect(self.update_by_trigger)
        self.Trigger[1].valueChanged.connect(self.update_by_trigger)
        self.TriggerCB[0].stateChanged.connect(self.update_by_trigger)
        self.TriggerCB[1].stateChanged.connect(self.update_by_trigger)
        self.TriggerSlope[0].currentIndexChanged.connect(self.update_by_trigger)
        self.TriggerSlope[1].currentIndexChanged.connect(self.update_by_trigger)

        self.WinType.currentIndexChanged.connect(self.update_fig_f)
        self.fftN.valueChanged.connect(self.update_fig_f)
        self.fCursorCB.stateChanged.connect(self.update_fig_f)
        self.fLogCB.stateChanged.connect(self.update_fig_f)
        self.ALogCB.stateChanged.connect(self.update_fig_f)
        self.fZoom.valueChanged.connect(self.update_fig_f)
        self.fYLim[0].valueChanged.connect(self.update_fig_f)
        self.fYLim[1].valueChanged.connect(self.update_fig_f)
        self.fPos.valueChanged.connect(self.update_fig_f)

    @pyqtSlot()
    def on_RunButton_clicked(self):
        self.RUNNING = not self.RUNNING
        # print(self.RUNNING)
        if self.RUNNING:
            self.RunButton.setText("Stop")
            self.threads[0].start()
            self.threads[1].start()
        else:
            self.RunButton.setText("Run")
            self.threads[0].quit()
            self.threads[1].quit()

    def update_trig_time(self):
        self.TRIGT = time.perf_counter()
        if not self.RUNNING:
            self.plot_fig_t()

    # 用于暂停状态下刷新图像
    def update_fig_t(self):
        if not self.RUNNING:
            self.plot_fig_t()

    def update_fig_f(self):
        if not self.RUNNING:
            self.plot_fig_f()

    def update_fig(self):
        if not self.RUNNING:
            self.plot_fig_t()
            self.plot_fig_f()

    def update_by_cursor(self):
        if not self.RUNNING:
            if self.CursorTarget.currentText() == 0:
                self.plot_fig_t()
            else:
                self.plot_fig_f()

    def update_by_trigger(self):
        if not self.RUNNING:
            pos = self.trigger()
            self.disp_len = int(self.CHUNK / self.tZoom.value())
            self.disp_sig[0] = self.rec_y[0][pos[0] : pos[0] + self.disp_len]
            self.disp_sig[1] = self.rec_y[1][pos[1] : pos[1] + self.disp_len]
            self.plot_fig_t()

    def plot_fig_t(self):
        # if self.RUNNING:

        channel = self.Channel.currentIndex()

        if channel == 3:
            self.fig_t.ax.clear()
            # self.fig_t.ax.plot(
            #     self.tYZoom[0].value() * self.disp_sig[0] + self.Offset[0].value(),
            #     self.tYZoom[1].value() * self.disp_sig[1] + self.Offset[1].value(),
            #     c="yellow",
            # )
            self.fig_t.ax.plot(
                self.tYZoom[0].value() * self.disp_sig[0] + self.Offset[0].value(),
                self.tYZoom[1].value() * self.disp_sig[1] + self.Offset[1].value(),
                c="yellow",
            )
            self.fig_t.ax.axis("equal")
            self.fig_t.draw()
            return

        t_max = self.T[self.disp_len - 1]

        # 计算光标
        X = [c.value() for c in self.CursorX]
        Y = [c.value() for c in self.CursorY]
        if self.CursorTarget.currentIndex() == 0:
            cid = self.MeasChan.currentIndex()
            self.TX = [v * t_max for v in X]
            self.TY = [v * 20 - 10 for v in Y]

        # 计算测量值
        cid = self.MeasChan.currentIndex()
        X0 = self.TX[0] * 1000
        X1 = self.TX[1] * 1000
        Y0 = (self.TY[0] - self.Offset[cid].value()) / self.tYZoom[cid].value()
        Y1 = (self.TY[1] - self.Offset[cid].value()) / self.tYZoom[cid].value()
        digits = 3

        # 显示时域信号
        self.fig_t.ax.clear()
        if channel == 0 or channel == 1:
            self.fig_t.ax.plot(
                self.T[: self.disp_len],
                self.tYZoom[0].value() * self.disp_sig[0] + self.Offset[0].value(),
                c=self.fig_t.c[0],
            )
        if channel == 0 or channel == 2:
            self.fig_t.ax.plot(
                self.T[: self.disp_len],
                self.tYZoom[1].value() * self.disp_sig[1] + self.Offset[1].value(),
                c=self.fig_t.c[1],
            )

        # 显示触发电平
        if time.perf_counter() - self.TRIGT <= 5:
            self.fig_t.ax.axhline(y=self.Trigger[0].value(), ls="--", c="orange")
            self.fig_t.ax.axhline(y=self.Trigger[1].value(), ls="--", c="orange")

        # 绘制时域光标
        if self.CursorCB.checkState():
            self.fig_t.ax.axhline(y=self.TY[0], ls="--", c="orange")
            self.fig_t.ax.axhline(y=self.TY[1], ls="--", c="orange")
            self.fig_t.ax.axvline(x=self.TX[0], ls="--", c="orange")
            self.fig_t.ax.axvline(x=self.TX[1], ls="--", c="orange")

        self.fig_t.ax.axis("auto")  # axis equal后重置坐标轴
        self.fig_t.ax.set_xlim((0, t_max))
        self.fig_t.ax.set_ylim((-10, 10))

        # 将横纵坐标分为10x10的网格
        self.fig_t.ax.xaxis.set_ticks(np.linspace(0, t_max, 11))
        self.fig_t.ax.yaxis.set_ticks(np.linspace(-10, 10, 11))
        self.fig_t.ax.grid(c="gray")

        # 显示GND位置
        self.fig_t.ax_left.clear()
        self.fig_t.ax_left.axhline(
            y=(self.Offset[0].value() + 10) / 20, c=self.fig_t.c[0]
        )
        self.fig_t.ax_left.axhline(
            y=(self.Offset[1].value() + 10) / 20, c=self.fig_t.c[1]
        )

        # 显示span
        self.fig_t.data["t"].set_text(str(round(1000 * t_max / 10, 4)) + "ms/")
        self.fig_t.data["1"].set_text(str(2 / self.tYZoom[0].value()) + "V/")
        self.fig_t.data["2"].set_text(str(2 / self.tYZoom[1].value()) + "V/")

        # 显示时域测量结果
        self.fig_t.data["t1"].set_text(str(round(X0, digits)))
        self.fig_t.data["t2"].set_text(str(round(X1, digits)))
        self.fig_t.data["dt"].set_text(str(round(X1 - X0, digits)))
        if X1 != X0:
            self.fig_t.data["1/dt"].set_text(str(round(1000 / abs(X1 - X0), digits)))
        else:
            self.fig_t.data["1/dt"].set_text("Inf")
        self.fig_t.data["Y1"].set_text(str(round(Y0, digits)))
        self.fig_t.data["Y2"].set_text(str(round(Y1, digits)))
        self.fig_t.data["dY"].set_text(str(round(Y1 - Y0, digits)))

        self.fig_t.draw()

    def plot_fig_f(self):
        channel = self.Channel.currentIndex()

        nfft = self.fftN.value()
        num = nfft // 2 + 1
        f = np.linspace(0, self.f_max, num)
        disp_n = num // self.fZoom.value()
        disp_i = int(self.fPos.value() * (num - disp_n))

        f_log = self.fLogCB.checkState()
        f_lim = [f[disp_i], f[disp_i + disp_n - 1]]
        if f_log and f_lim[0] == 0:
            f_lim[0] = 1

        win_type = self.WinType.currentIndex()
        sig_L = len(self.rec_y[0])
        if win_type == 0:
            window = np.hanning(sig_L)
        elif win_type == 1:
            window = np.hamming(sig_L)
        elif win_type == 2:
            window = np.blackman(sig_L)
        elif win_type == 3:
            window = np.bartlett(sig_L)
        else:
            window = np.ones(sig_L)
        if self.RUNNING:
            FFT = [np.fft.rfft(window * self.rec_y[i], n=nfft) / sig_L for i in [0, 1]]
            if self.ALogCB.checkState():
                self.disp_FFT = [
                    20 * np.log10(np.abs(FFT[0]) + 1e-6),
                    20 * np.log10(np.abs(FFT[1]) + 1e-6),
                ]
            else:
                self.disp_FFT = [np.abs(FFT[0]), np.abs(FFT[1])]

        if self.fYLim[0].value() < self.fYLim[1].value():
            y_lim = [self.fYLim[i].value() for i in [0, 1]]
        else:
            y_lim = [
                int(min(np.min(self.disp_FFT[0]), np.min(self.disp_FFT[1]))) - 1,
                int(max(np.max(self.disp_FFT[0]), np.max(self.disp_FFT[1]))) + 1,
            ]

        if self.CursorTarget.currentIndex() == 1:
            # if f_log:
            #     a, b = (f_lim[1] - f_lim[0]) / 9, f_lim[0] - (f_lim[1] - f_lim[0]) / 9
            #     self.FX = [a * 10 ** self.CursorX[i].value() + b for i in [0, 1]]
            self.FX = [
                self.CursorX[i].value() * (f_lim[1] - f_lim[0]) + f_lim[0]
                for i in [0, 1]
            ]
            self.FY = [
                self.CursorY[i].value() * (y_lim[1] - y_lim[0]) + y_lim[0]
                for i in [0, 1]
            ]

        # 显示FFT
        self.fig_f.ax.clear()
        if self.fLogCB.checkState():
            self.fig_f.ax.set_xscale("log")
        if channel != 2:
            self.fig_f.ax.plot(f, self.disp_FFT[0], c=self.fig_f.c[0])
        if channel != 1:
            self.fig_f.ax.plot(f, self.disp_FFT[1], c=self.fig_f.c[1])

        # 显示光标
        if self.fCursorCB.checkState():
            self.fig_f.ax.axvline(x=self.FX[0], ls="--", c="orange")
            self.fig_f.ax.axvline(x=self.FX[1], ls="--", c="orange")
            self.fig_f.ax.axhline(y=self.FY[0], ls="--", c="orange")
            self.fig_f.ax.axhline(y=self.FY[1], ls="--", c="orange")

        # 坐标轴调整
        self.fig_f.ax.set_ylim((y_lim[0], y_lim[1]))
        self.fig_f.ax.set_xlim((f_lim[0], f_lim[1]))
        # self.fig_f.ax.set_yticks(np.arange(self.y_lim[0], self.y_lim[1] + 1, 5))
        # self.fig_f.ax.set_xticks(np.linspace(f_lim[0], f_lim[1], 20))
        # self.fig_f.ax.tick_params(color="white", labelcolor="white")

        # 展示测量结果
        self.fig_f.data["f1"].set_text(str(round(self.FX[0], 2)))
        self.fig_f.data["f2"].set_text(str(round(self.FX[1], 2)))
        self.fig_f.data["Y1"].set_text(str(round(self.FY[0], 2)))
        self.fig_f.data["Y2"].set_text(str(round(self.FY[1], 2)))
        self.fig_f.data["df"].set_text(str(round(self.FX[1] - self.FX[0], 2)))
        self.fig_f.data["dY"].set_text(str(round(self.FY[1] - self.FY[0], 2)))

        self.fig_f.draw()

    def callback(self, in_data, frame_count, time_info, status):
        data = self.sg.play_bytes
        # print(self.UPDATE_PLAYBYTES)
        self.UPDATE_PLAYBYTES = True
        # print((time.perf_counter() - self.tmp) * 44100)
        # self.tmp = time.perf_counter()
        self.rec_bytes = in_data
        return (data, paContinue)

    def trigger(self):
        tgcb = [self.TriggerCB[0].checkState(), self.TriggerCB[1].checkState()]
        idx = [0, 0]

        for cid in [0, 1]:
            tgv = self.Trigger[cid].value()
            slope = 1 - 2 * self.TriggerSlope[cid].currentIndex()
            y = self.tYZoom[cid].value() * self.rec_y[cid] + self.Offset[cid].value()
            if tgcb[cid]:
                for i in range(1, len(y)):
                    if (y[i] - tgv) * slope >= 0 and (y[i - 1] - tgv) * slope < 0:
                        idx[cid] = i
                        break
                if len(y) - idx[cid] < self.disp_len:
                    idx[cid] = 0
        if tgcb[0] and not tgcb[1]:
            idx[1] = idx[0]
        elif tgcb[1] and not tgcb[0]:
            idx[0] = idx[1]
        return idx

    def run(self):
        pa = PyAudio()
        stream = pa.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            stream_callback=self.callback,
            frames_per_buffer=self.CHUNK,
        )
        stream.start_stream()

        while self.RUNNING:
            # t1 = time.perf_counter()
            if self.rec_bytes:
                sig = np.frombuffer(self.rec_bytes, dtype=np.int16) / 32768
                self.rec_y[0] = self.input_gain * sig[::2]
                self.rec_y[1] = self.input_gain * sig[1::2]
                self.rec_bytes = bytes()

            # sig = np.c_[
            #     5
            #     * (sin(2 * pi * 100 * self.T) + 0.1 * (-1) ** np.arange(self.CHUNK))
            #     / self.factor,
            #     5
            #     * (cos(2 * pi * 100 * self.T) + 0.1 * (-1) ** np.arange(self.CHUNK))
            #     / self.factor,
            # ].flatten()

            # sig = np.repeat(sin(2 * pi * 1000 * self.T), 2)

            self.disp_len = int(self.CHUNK / self.tZoom.value())

            pos = self.trigger()

            self.disp_sig[0] = self.rec_y[0][pos[0] : pos[0] + self.disp_len]
            self.disp_sig[1] = self.rec_y[1][pos[1] : pos[1] + self.disp_len]

            if self.UPDATE_PLAYBYTES:
                self.sg.update_sig()
                self.UPDATE_PLAYBYTES = False

            # self.plot_fig_t()
            # self.plot_fig_f()

            # print(time.perf_counter() - t1)

        stream.stop_stream()
        stream.close()
        pa.terminate()
        self.sg.play_y = np.zeros(self.CHUNK * 2)
        self.sg.play_bytes = np.zeros(self.CHUNK * 2, dtype=np.int16).tobytes()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    # p = Process(target=win.plot_fig_t)
    # p.start()
    t = Thread(target=win.plot_fig_t)
    t.start()
    win.show()
    sys.exit(app.exec_())
    t.terminate()
