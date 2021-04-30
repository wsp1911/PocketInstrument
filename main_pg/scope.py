# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QThread, QTimer
import numpy as np
from numpy import pi, sin, cos
import sys, time
from Ui_scope import Ui_scope
from SignalGenerator import SignalGenerator
from sigGenerate import getWave

# from SignalGenerator import SignalGenerator
# from BodePlotter import BodePlotter

import wave
from pyaudio import PyAudio, paInt16, paContinue

from scipy.io import savemat
from scipy import signal


class worker(QObject):
    def __init__(self, parent=None, win=None):
        super(worker, self).__init__(parent=parent)
        self.win = win

    def run(self):
        self.win.run()


# class for the application window
class AppWindow(Ui_scope):
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
        self.disp_FFT = [
            np.zeros(self.fftN.value() // 2 + 1),
            np.zeros(self.fftN.value() // 2 + 1),
        ]

        self.TX, self.TY, self.FX, self.FY = ([0, 1], [0, 1], [0, 1], [0, 1])

        self.RUNNING = False
        self.EXIT = False
        self.UPDATE = [False, False]
        self.TRIGT = time.perf_counter() - 5

        self.UPDATE_PLAYBYTES = False

        self.sg = SignalGenerator(parent=self, chunk=self.CHUNK, rate=self.RATE)

        self.worker = worker(win=self)
        self.process_thread = QThread()

        self.worker.moveToThread(self.process_thread)

        # self.Bode_plotter = BodePlotter()

        self.tb_actions = self.toolbar.actions()

        self.connect()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plt_tf)
        self.timer.start(50)
        self.t_t = []
        self.t_f = []

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

        self.process_thread.started.connect(self.worker.run)

        self.Trigger[0].valueChanged.connect(self.update_trig_time)
        self.Trigger[1].valueChanged.connect(self.update_trig_time)

        self.tZoom.valueChanged.connect(self.update_disp_sig_WNR)  # 显示长度改变后防止越界需要再触发
        self.Trigger[0].valueChanged.connect(self.update_disp_sig_WNR)
        self.Trigger[1].valueChanged.connect(self.update_disp_sig_WNR)
        self.TriggerCB[0].stateChanged.connect(self.update_disp_sig_WNR)
        self.TriggerCB[1].stateChanged.connect(self.update_disp_sig_WNR)
        self.TriggerSlope[0].currentIndexChanged.connect(self.update_disp_sig_WNR)
        self.TriggerSlope[1].currentIndexChanged.connect(self.update_disp_sig_WNR)

        self.fftN.valueChanged.connect(self.update_disp_FFT_WNR)
        self.WinType.currentIndexChanged.connect(self.update_disp_FFT_WNR)
        self.ALogCB.stateChanged.connect(self.update_disp_FFT_WNR)

    @pyqtSlot()
    def on_RunButton_clicked(self):
        self.RUNNING = not self.RUNNING
        if self.RUNNING:
            self.RunButton.setText("Stop")
            self.process_thread.start()
        else:
            self.RunButton.setText("Run")
            self.process_thread.quit()

    # WNR: when not running
    def update_disp_sig_WNR(self):
        if not self.RUNNING:
            self.update_disp_sig()

    def update_disp_sig(self):
        self.disp_len = int(self.CHUNK / self.tZoom.value())
        pos = self.trigger()
        self.disp_sig[0] = self.rec_y[0][pos[0] : pos[0] + self.disp_len]
        self.disp_sig[1] = self.rec_y[1][pos[1] : pos[1] + self.disp_len]

    def update_disp_FFT_WNR(self):
        if not self.RUNNING:
            self.update_disp_FFT()

    def update_disp_FFT(self):

        nfft = self.fftN.value()

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

        FFT = [np.fft.rfft(window * self.rec_y[i], n=nfft) / sig_L for i in [0, 1]]
        if self.ALogCB.checkState():
            self.disp_FFT = [
                20 * np.log10(np.abs(FFT[0]) + 1e-6),
                20 * np.log10(np.abs(FFT[1]) + 1e-6),
            ]
        else:
            self.disp_FFT = [np.abs(FFT[0]), np.abs(FFT[1])]

    def update_trig_time(self):
        self.TRIGT = time.perf_counter()

    def update_plt_tf(self):
        self.update_plt_t()
        self.update_plt_f()

    def update_plt_t(self):
        if self.RUNNING:
            t1 = time.perf_counter()
        else:
            t1 = 0

        channel = self.Channel.currentIndex()

        if channel == 3:
            self.pwt.curve[0].setData()
            self.pwt.curve[1].setData()
            self.pwt.curve[2].setData(
                self.tYZoom[0].value() * self.disp_sig[0] + self.Offset[0].value(),
                self.tYZoom[1].value() * self.disp_sig[1] + self.Offset[1].value(),
            )
            self.pwt.setAspectLocked()
            return

        t_max = self.T[self.disp_len - 1]

        # 计算光标
        X = [c.value() for c in self.CursorX]
        Y = [c.value() for c in self.CursorY]
        if self.CursorTarget.currentIndex() == 0:
            self.TX = [v * t_max for v in X]
            self.TY = [v * 20 - 10 for v in Y]

        # 显示时域信号
        self.pwt.setAspectLocked(False)
        self.pwt.curve[2].setData()
        if channel == 0:
            self.pwt.curve[0].setData(
                self.T[: self.disp_len],
                self.tYZoom[0].value() * self.disp_sig[0] + self.Offset[0].value(),
            )
            self.pwt.curve[1].setData(
                self.T[: self.disp_len],
                self.tYZoom[1].value() * self.disp_sig[1] + self.Offset[1].value(),
            )
        elif channel == 1:
            self.pwt.curve[1].setData()
            self.pwt.curve[0].setData(
                self.T[: self.disp_len],
                self.tYZoom[0].value() * self.disp_sig[0] + self.Offset[0].value(),
            )
        elif channel == 2:
            self.pwt.curve[0].setData()
            self.pwt.curve[1].setData(
                self.T[: self.disp_len],
                self.tYZoom[1].value() * self.disp_sig[1] + self.Offset[1].value(),
            )

        # 显示触发电平
        if time.perf_counter() - self.TRIGT <= 3:
            self.pwt.trigger[0].setData(
                [0, t_max], [self.Trigger[0].value(), self.Trigger[0].value()]
            )
            self.pwt.trigger[1].setData(
                [0, t_max], [self.Trigger[1].value(), self.Trigger[1].value()]
            )
        else:
            self.pwt.trigger[0].setData()
            self.pwt.trigger[1].setData()

        # 绘制时域光标
        if self.CursorCB.checkState():
            self.pwt.hline[0].setData([0, t_max], [self.TY[0], self.TY[0]])
            self.pwt.hline[1].setData([0, t_max], [self.TY[1], self.TY[1]])
            self.pwt.vline[0].setData([self.TX[0], self.TX[0]], [-10, 10])
            self.pwt.vline[1].setData([self.TX[1], self.TX[1]], [-10, 10])
        else:
            self.pwt.hline[0].setData()
            self.pwt.hline[1].setData()
            self.pwt.vline[0].setData()
            self.pwt.vline[1].setData()

        self.pwt.setXRange(0, t_max)

        # 计算测量值
        cid = self.MeasChan.currentIndex()
        X0 = self.TX[0] * 1000
        X1 = self.TX[1] * 1000
        Y0 = (self.TY[0] - self.Offset[cid].value()) / self.tYZoom[cid].value()
        Y1 = (self.TY[1] - self.Offset[cid].value()) / self.tYZoom[cid].value()
        digits = 3

        # 显示时域测量结果
        if self.DataDispCB.checkState():
            self.DataDispGrid[0].setData("t1/ms", str(round(X0, digits)))
            self.DataDispGrid[0].setData("t2/ms", str(round(X1, digits)))
            self.DataDispGrid[0].setData("dt/ms", str(round(X1 - X0, digits)))
            if X1 != X0:
                self.DataDispGrid[0].setData(
                    "1/dt/ms", str(round(1000 / abs(X1 - X0), digits))
                )
            else:
                self.DataDispGrid[0].setData("1/dt/ms", "Inf")
            self.DataDispGrid[0].setData("Y1/V", str(round(Y0, digits)))
            self.DataDispGrid[0].setData("Y2/V", str(round(Y1, digits)))
            self.DataDispGrid[0].setData("dY/V", str(round(Y1 - Y0, digits)))

        if t1 != 0:
            self.t_t.append(time.perf_counter() - t1)
        # print("t1=%f" % t2)

    def update_plt_f(self):
        if self.RUNNING:
            t1 = time.perf_counter()
        else:
            t1 = 0

        channel = self.Channel.currentIndex()
        nfft = self.fftN.value()
        num = nfft // 2 + 1

        f = np.linspace(0, self.f_max, num)
        disp_n = num // self.fZoom.value()
        disp_i = int(self.fPos.value() * (num - disp_n))
        f_log = self.fLogCB.checkState()
        f_lim = [f[disp_i], f[disp_i + disp_n - 1]]
        if f_log:
            f_lim[0] = np.log10(f_lim[0]) if f_lim[0] > 0 else 0.8
            f_lim[1] = np.log10(f_lim[1])

        if self.fYLim[0].value() < self.fYLim[1].value():
            y_lim = [self.fYLim[i].value() for i in [0, 1]]
        else:
            y_lim = [
                int(min(np.min(self.disp_FFT[0]), np.min(self.disp_FFT[1]))) - 1,
                int(max(np.max(self.disp_FFT[0]), np.max(self.disp_FFT[1]))) + 1,
            ]

        if self.CursorTarget.currentIndex() == 1:
            self.FX = [
                self.CursorX[i].value() * (f_lim[1] - f_lim[0]) + f_lim[0]
                for i in [0, 1]
            ]
            self.FY = [
                self.CursorY[i].value() * (y_lim[1] - y_lim[0]) + y_lim[0]
                for i in [0, 1]
            ]

        # 显示FFT
        if f_log:
            self.pwf.curve[0].setLogMode(True, False)
            self.pwf.curve[1].setLogMode(True, False)
        else:
            self.pwf.curve[0].setLogMode(False, False)
            self.pwf.curve[1].setLogMode(False, False)

        if channel in [0, 3]:
            self.pwf.curve[0].setData(f, self.disp_FFT[0])
            self.pwf.curve[1].setData(f, self.disp_FFT[1])
        elif channel == 1:
            self.pwf.curve[0].setData(f, self.disp_FFT[0])
            self.pwf.curve[1].setData()
        elif channel == 2:
            self.pwf.curve[0].setData()
            self.pwf.curve[1].setData(f, self.disp_FFT[1])

        # 显示光标
        if self.fCursorCB.checkState():
            self.pwf.vline[0].setData([self.FX[0], self.FX[0]], [y_lim[0], y_lim[1]])
            self.pwf.vline[1].setData([self.FX[1], self.FX[1]], [y_lim[0], y_lim[1]])
            self.pwf.hline[0].setData([f_lim[0], f_lim[1]], [self.FY[0], self.FY[0]])
            self.pwf.hline[1].setData([f_lim[0], f_lim[1]], [self.FY[1], self.FY[1]])
        else:
            self.pwf.vline[0].setData()
            self.pwf.vline[1].setData()
            self.pwf.hline[0].setData()
            self.pwf.hline[1].setData()

        # 坐标轴调整
        self.pwf.setYRange(y_lim[0], y_lim[1])
        self.pwf.setXRange(f_lim[0], f_lim[1])
        # print("t3=%f" % (time.perf_counter() - t3))

        # 展示测量结果
        if f_log and max(self.FX[0], self.FX[1]) < 10:
            self.FX = [10 ** x for x in self.FX]
        if self.DataDispCB.checkState():
            self.DataDispGrid[1].setData("f1/Hz", str(round(self.FX[0], 2)))
            self.DataDispGrid[1].setData("f2/Hz", str(round(self.FX[1], 2)))
            self.DataDispGrid[1].setData("Y1/dB", str(round(self.FY[0], 2)))
            self.DataDispGrid[1].setData("Y2/dB", str(round(self.FY[1], 2)))
            self.DataDispGrid[1].setData(
                "df/Hz", str(round(self.FX[1] - self.FX[0], 2))
            )
            self.DataDispGrid[1].setData(
                "dY/dB", str(round(self.FY[1] - self.FY[0], 2))
            )

        if t1 != 0:
            self.t_f.append(time.perf_counter() - t1)

    def callback(self, in_data, frame_count, time_info, status):
        data = self.sg.play_bytes
        self.UPDATE_PLAYBYTES = True
        self.rec_bytes = in_data
        return (data, paContinue)

    def trigger(self):
        tgcb = [self.TriggerCB[0].checkState(), self.TriggerCB[1].checkState()]
        idx = [0, 0]
        for cid in [0, 1]:
            if tgcb[cid]:
                tgv = self.Trigger[cid].value()
                slope = 1 - 2 * self.TriggerSlope[cid].currentIndex()
                y = -np.abs(
                    self.rec_y[cid][1 : -self.disp_len]
                    + (self.Offset[cid].value() - tgv) / self.tYZoom[cid].value()
                )
                pks = signal.find_peaks(y)
                for i in pks[0]:  # y1从y的1处开始，还原坐标时要加回去
                    if (self.rec_y[cid][i + 1] - self.rec_y[cid][i]) * slope > 0:
                        idx[cid] = i
                        break

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

        print_t = True
        t_list = []
        while self.RUNNING:
            t_list.append([])
            t1 = time.perf_counter()
            # receive new data
            if self.rec_bytes:
                sig = np.frombuffer(self.rec_bytes, dtype=np.int16) / 32768
                self.rec_y[0] = self.input_gain * sig[::2]
                self.rec_y[1] = self.input_gain * sig[1::2]
                self.rec_bytes = bytes()
            t_list[-1].append(time.perf_counter() - t1)

            t1 = time.perf_counter()

            # sig = np.c_[
            #     5
            #     * (sin(2 * pi * 100 * self.T) + 0.1 * (-1) ** np.arange(self.CHUNK))
            #     / self.factor,
            #     5
            #     * (cos(2 * pi * 100 * self.T) + 0.1 * (-1) ** np.arange(self.CHUNK))
            #     / self.factor,
            # ].flatten()

            # sig = np.repeat(sin(2 * pi * 1000 * self.T), 2)

            # send new data
            if self.UPDATE_PLAYBYTES:
                self.sg.update_sig()
                self.UPDATE_PLAYBYTES = False

            t_list[-1].append(time.perf_counter() - t1)

            t1 = time.perf_counter()
            # update disp_sig
            self.update_disp_sig()

            t_list[-1].append(time.perf_counter() - t1)

            t1 = time.perf_counter()

            # update disp_FFT
            self.update_disp_FFT()

            # self.update_plt_t()
            # self.update_plt_f()

            t_list[-1].append(time.perf_counter() - t1)

        stream.stop_stream()
        stream.close()
        pa.terminate()

        self.sg.reset()

        if print_t:
            t1 = 1000 * np.mean(np.array(t_list), axis=0)
            print("rec     :%f" % t1[0])
            print("send    :%f" % t1[1])
            print("disp_sig:%f" % t1[2])
            print("FFT     :%f" % t1[3])
            print("plt_t   :%f" % (1000 * np.mean(np.array(self.t_t))))
            print("plt_f   :%f" % (1000 * np.mean(np.array(self.t_f))))
            self.t_t = []
            self.t_f = []


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec_())
