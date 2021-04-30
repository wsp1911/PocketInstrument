# -*- coding: utf-8 -*-
import sys, os

sys.path.append(os.getcwd())

import matplotlib

# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSlot
import numpy as np
from pyaudio import PyAudio, paInt16, paContinue

from Ui_bp import Ui_MainWindow

from cal import get_chunk, get_response
from public.public import save_data


matplotlib.use("Qt5Agg")
# normalized for 中文显示和负号
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

# 对数坐标指数出现负数正常显示
matplotlib.rcParams.update(
    {
        "text.usetex": False,
        "font.family": "stixgeneral",
        "mathtext.fontset": "stix",
    }
)


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
        self.y = 0
        self.rec_y = bytes()

        self.f = np.array([])
        self.A = np.array([])
        self.phi = np.array([])

        self.MEASURING = False

        self.connect()

    def connect(self):
        self.CursorF[0].valueChanged.connect(self.plot_fig)
        self.CursorF[1].valueChanged.connect(self.plot_fig)
        self.CursorA.valueChanged.connect(self.plot_fig)
        self.CursorPhi.valueChanged.connect(self.plot_fig)
        self.fLogCB.stateChanged.connect(self.plot_fig)
        self.ALogCB.stateChanged.connect(self.plot_fig)
        self.CursorCB.stateChanged.connect(self.plot_fig)
        self.ValueCB.stateChanged.connect(self.plot_fig)
        self.fmin.valueChanged.connect(self.plot_fig)
        self.fmax.valueChanged.connect(self.plot_fig)

    @pyqtSlot()
    def on_ResetButton_clicked(self):
        if not self.MEASURING:
            self.response = 0
            self.fig.ax_A.clear()
            self.fig.ax_phi.clear()
            self.fig.draw()

    @pyqtSlot()
    def on_dataSave_clicked(self):
        if not self.MEASURING:
            save_data(
                self.filename.text(),
                np.array([self.f, self.A, self.phi]).T,
                self.dataFormat.currentText(),
            )

    @pyqtSlot()
    def on_imgSave_clicked(self):
        if not self.MEASURING:
            self.fig.fig.savefig(self.filename.text() + self.imgFormat.currentText())

    def plot_fig(self):
        if not self.MEASURING:
            self.fig.ax_A.clear()
            self.fig.ax_phi.clear()
            if self.fLogCB.checkState():
                self.fig.ax_A.set_xscale("log")
                self.fig.ax_phi.set_xscale("log")
            if self.ALogCB.checkState():
                self.fig.ax_A.set_yscale("log")
            if len(self.f) != 0:
                self.fig.ax_A.plot(self.f, self.A, "x", c="r")
                self.fig.ax_A.plot(self.f, self.A)
                self.fig.ax_phi.plot(self.f, self.phi, "x", c="r")
                self.fig.ax_phi.plot(self.f, self.phi)
                if self.ValueCB.checkState():
                    for x, y1, y2 in zip(self.f, self.A, self.phi):
                        self.fig.ax_A.text(
                            x, y1, str(round(x, 1)) + " " + str(round(y1, 2))
                        )
                        self.fig.ax_phi.text(
                            x, y2, str(round(x, 1)) + " " + str(round(y2, 1))
                        )
            fmin, fmax = self.fmin.value(), self.fmax.value()
            if fmin < fmax:
                self.fig.ax_A.set_xlim((fmin, fmax))
                self.fig.ax_phi.set_xlim((fmin, fmax))
            if self.CursorCB.checkState():
                f_lim = self.fig.ax_A.get_xlim()
                A_lim = self.fig.ax_A.get_ylim()
                phi_lim = self.fig.ax_phi.get_ylim()
                cur_f = [
                    self.CursorF[i].value() * (f_lim[1] - f_lim[0]) + f_lim[0]
                    for i in range(2)
                ]
                cur_A = self.CursorA.value() * (A_lim[1] - A_lim[0]) + A_lim[0]
                cur_phi = (
                    self.CursorPhi.value() * (phi_lim[1] - phi_lim[0]) + phi_lim[0]
                )
                self.fig.ax_A.axvline(x=cur_f[0], c="orange", ls="--")
                self.fig.ax_A.axhline(y=cur_A, c="orange", ls="--")
                self.fig.ax_phi.axvline(x=cur_f[1], c="orange", ls="--")
                self.fig.ax_phi.axhline(y=cur_phi, c="orange", ls="--")
                self.fig.ax_A.text(cur_f[0], A_lim[0], str(round(cur_f[0], 2)))
                self.fig.ax_A.text(f_lim[0], cur_A, str(round(cur_A, 3)))
                self.fig.ax_phi.text(cur_f[1], phi_lim[0], str(round(cur_f[1], 2)))
                self.fig.ax_phi.text(f_lim[0], cur_phi, str(round(cur_phi, 3)))
            self.fig.ax_A.set_xlabel("f/Hz")
            self.fig.ax_A.set_ylabel("A", rotation="horizontal")
            self.fig.ax_phi.set_xlabel("f/Hz")
            self.fig.ax_phi.set_ylabel(r"$\phi$", rotation="horizontal")
            self.fig.draw()

    def callback(self, in_data, frame_count, time_info, status):
        data = self.y
        self.rec_y += in_data
        return (data, paContinue)

    @pyqtSlot()
    def on_StartButton_clicked(self):
        self.MEASURING = True
        pa = PyAudio()
        if self.ScanType.currentIndex() == 0:
            fLeft, fRight, fNum = (
                self.fLeft.value(),
                self.fRight.value(),
                int(self.fNum.value()),
            )
            if fLeft > fRight:
                return
            f_arr = np.linspace(fLeft, fRight, fNum, endpoint=True)
        else:
            f_arr = np.array([self.fValue.value()])
            if f_arr[0] < 5 and f_arr != 0:
                return

        resp = dict(zip(self.f, zip(self.A, self.phi)))

        for f in f_arr:
            self.rec_y = bytes()
            cnt = 0
            self.CHUNK = get_chunk(f, self.RATE)
            t = np.arange(0, self.CHUNK / self.RATE, 1 / self.RATE)
            if f == 0:
                self.y = 0.5 * np.ones(len(t))
            else:
                self.y = 0.5 * np.sin(2 * np.pi * f * t)
            self.y = np.repeat(self.y, 2)
            self.y = (-self.y * 32768).astype(np.int16).tobytes()

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

            L_reg = 0
            while cnt < 2:
                rec_y_copy = self.rec_y
                if len(rec_y_copy) >= self.CHUNK * 4:
                    rec_data = (
                        np.fromstring(rec_y_copy[-4 * self.CHUNK :], dtype=np.int16)
                        / 32768
                    )
                    if np.max(rec_data) > 0.02 and L_reg != len(rec_y_copy):
                        L_reg = len(rec_y_copy)
                        cnt += 1

            stream.stop_stream()
            stream.close()  # 关闭

            rec_data = np.fromstring(self.rec_y, dtype=np.int16) / 32768
            y0 = rec_data[::2]
            y1 = rec_data[1::2]

            A, phi = get_response(f, self.RATE, self.CHUNK, y0, y1)

            resp[f] = (A, phi)

        resp_list = []
        for f in resp.keys():
            resp_list.append((f, resp[f][0], resp[f][1]))
        resp_arr = np.array(resp_list)
        resp_arr = resp_arr[np.argsort(resp_arr[:, 0])]
        self.f, self.A, self.phi = resp_arr[:, 0], resp_arr[:, 1], resp_arr[:, 2]
        if self.f[0] == 0 and len(self.f) > 1:
            if abs(self.phi[1]) < 10:
                self.phi[0] = 0
            elif 0 < 90 - self.phi[1] < 10:
                self.phi[0] = 90
            else:
                self.phi[0] = self.phi[1]

        self.MEASURING = False

        self.plot_fig()

        pa.terminate()  # 终结

    @pyqtSlot()
    def on_StartButton_clicked1(self):
        self.MEASURING = True
        if self.ScanType.currentIndex() == 0:
            fLeft, fRight, fNum = (
                self.fLeft.value(),
                self.fRight.value(),
                int(self.fNum.value()),
            )
            if fLeft > fRight:
                return
            f_arr = np.linspace(fLeft, fRight, fNum, endpoint=True)
        else:
            f_arr = np.array([self.fValue.value()])
            if f_arr[0] < 5 and f_arr != 0:
                return

        resp = dict(zip(self.f, zip(self.A, self.phi)))

        for f in f_arr:
            self.rec_y = bytes()
            cnt = 0
            self.CHUNK = get_chunk(f, self.RATE)
            t = np.arange(0, self.CHUNK / self.RATE, 1 / self.RATE)
            if f == 0:
                self.y = 0.5 * np.ones(len(t))
            else:
                self.y = 0.5 * np.sin(2 * np.pi * f * t)
            self.y = np.repeat(self.y, 2)
            self.y = (-self.y * 32768).astype(np.int16).tobytes()

            A, phi = 0.7 + np.random.rand() * 0.3, 45 + np.random.rand() * 45
            resp[f] = (A, phi)

        resp_list = []
        for f in resp.keys():
            resp_list.append((f, resp[f][0], resp[f][1]))
        resp_arr = np.array(resp_list)
        resp_arr = resp_arr[np.argsort(resp_arr[:, 0])]
        self.f, self.A, self.phi = resp_arr[:, 0], resp_arr[:, 1], resp_arr[:, 2]
        if self.f[0] == 0 and len(self.f) > 1:
            if abs(self.phi[1]) < 10:
                self.phi[0] = 0
            elif 0 < 90 - self.phi[1] < 10:
                self.phi[0] = 90
            else:
                self.phi[0] = self.phi[1]
        self.plot_fig()

        self.MEASURING = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec_())
