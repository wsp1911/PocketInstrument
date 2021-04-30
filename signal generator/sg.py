# -*- coding: utf-8 -*-
import matplotlib


# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt5.QtCore import pyqtSlot

import numpy as np
import sys, time

from Ui_SignalGenerator import Ui_SignalGenerator
from sigGenerate import getWave

# import wave
from pyaudio import PyAudio, paInt16, paContinue

from scipy.io import wavfile

import threading

matplotlib.use("Qt5Agg")

matplotlib.rcParams["figure.facecolor"] = "black"
matplotlib.rcParams["axes.facecolor"] = "black"
matplotlib.rcParams["axes.edgecolor"] = "gray"
matplotlib.rcParams["text.color"] = "white"
# normalized for 中文显示和负号
matplotlib.rcParams["font.sans-serif"] = ["SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False


class SignalGenerator(Ui_SignalGenerator):
    def __init__(self, parent=None):
        super(SignalGenerator, self).__init__(parent)

        self.factor = 1 / 15
        self.REFRESH = [False, False]
        self.rule = [
            [1, 2, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [2, 4],
            [1, 2, 4, 5],
        ]
        self.fs = 44100
        self.CHUNK = 1024
        self.data = np.zeros(self.CHUNK * 2)

        self.connect()

    def connect(self):
        self.waveSelect[0].currentIndexChanged.connect(lambda: self.refresh(0, -1))
        self.freqInput[0].valueChanged.connect(lambda: self.refresh(0, 0))
        self.ampInput[0].valueChanged.connect(lambda: self.refresh(0, 1))
        self.offsetInput[0].valueChanged.connect(lambda: self.refresh(0, 2))
        self.dutyInput[0].valueChanged.connect(lambda: self.refresh(0, 3))
        self.phiInput[0].valueChanged.connect(lambda: self.refresh(0, 4))
        self.waveSelect[1].currentIndexChanged.connect(lambda: self.refresh(1, -1))
        self.freqInput[1].valueChanged.connect(lambda: self.refresh(1, 0))
        self.ampInput[1].valueChanged.connect(lambda: self.refresh(1, 1))
        self.offsetInput[1].valueChanged.connect(lambda: self.refresh(1, 2))
        self.dutyInput[1].valueChanged.connect(lambda: self.refresh(1, 3))
        self.phiInput[1].valueChanged.connect(lambda: self.refresh(1, 4))

    # 0, sin, square, DC, triangle, sawtooth, exp, file
    # 0,   1,      2,  3,        4,        5,   6,    7
    def refresh(self, c_id, var_id):
        if var_id == -1:
            self.REFRESH[c_id] = True
        elif self.waveSelect[c_id].currentIndex() in self.rule[var_id]:
            self.REFRESH[c_id] = True

    @pyqtSlot(int)
    def on_synchSelect_currentIndexChanged(self):
        # print(0)
        if self.synchSelect.currentIndex() == 1:
            self.REFRESH[0] = True
            self.REFRESH[1] = True

    def play(self):
        pa = PyAudio()
        stream = pa.open(
            format=paInt16,
            channels=2,
            rate=44100,
            output=True,
        )

        y = [0, 0]
        i, j = 0, 0
        while True:
            # Synchronous
            wave_type = (
                self.waveSelect[0].currentIndex(),
                self.waveSelect[1].currentIndex(),
            )
            y[0] = getWave(
                wave_type[0],
                self.CHUNK,
                self.factor,
                self.fs,
                self.freqInput[0].value(),
                self.ampInput[0].value(),
                self.dutyInput[0].value() / 100,
                self.offsetInput[0].value(),
                self.phiInput[0].value(),
                self.expInput[0].text(),
                self.fileInput[0].text(),
            )
            y[1] = getWave(
                wave_type[1],
                self.CHUNK,
                self.factor,
                self.fs,
                self.freqInput[1].value(),
                self.ampInput[1].value(),
                self.dutyInput[1].value() / 100,
                self.offsetInput[1].value(),
                self.phiInput[1].value(),
                self.expInput[1].text(),
                self.fileInput[1].text(),
            )

            for id in [0, 1]:
                self.fig[id].ax.cla()
                self.fig[id].set_ax()
                if type(y[id]) == bool:
                    self.fig[id].ax.plot([0, 1], [0.5, 0.5], c="r")
                    y[id] = np.zeros(self.CHUNK)
                elif wave_type[id] == 7:
                    self.fig[id].ax.plot(
                        np.linspace(0, 1, num=len(y[id])),
                        y[id] / 2 + 0.5,
                    )
                else:
                    self.fig[id].ax.plot(
                        np.linspace(0, 1, num=2 * len(y[id])),
                        np.tile((y[id] / 2 + 0.5), 2),
                    )
                self.fig[id].draw()

            while True:
                for k in range(self.CHUNK):
                    self.data[2 * k] = y[0][i]
                    self.data[2 * k + 1] = y[1][j]
                    i, j = (i + 1) % len(y[0]), (j + 1) % len(y[1])
                y_bytes = (self.data * 32768).astype(np.int16).tobytes()
                stream.write(y_bytes)
                if self.REFRESH[0]:
                    self.REFRESH[0] = False
                    if self.synchSelect.currentIndex() == 1:
                        i, j = 0, 0
                    else:
                        i = 0
                    break
                if self.REFRESH[1]:
                    self.REFRESH[1] = False
                    if self.synchSelect.currentIndex() == 1:
                        i, j = 0, 0
                    else:
                        j = 0
                    break

        stream.stop_stream()
        stream.close()  # 关闭
        pa.terminate()  # 终结


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SignalGenerator()
    win.show()
    t1 = threading.Thread(target=win.play)
    t1.start()
    sys.exit(app.exec_())
