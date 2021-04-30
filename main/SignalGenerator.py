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
    def __init__(self, parent=None, chunk=2048, rate=44100):
        super(SignalGenerator, self).__init__(parent)

        self.REFRESH = [False, False]
        self.rule = [
            [1, 2, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [2, 4],
            [1, 2, 4, 5],
        ]
        self.CHUNK = chunk
        self.RATE = rate
        self.output_gain = 1 / 15
        self.idx = [0, 0]
        self.wave_type = [0, 0]
        self.sig = [np.zeros(self.CHUNK), np.zeros(self.CHUNK)]
        self.play_y = np.zeros(self.CHUNK * 2)
        self.play_bytes = np.zeros(self.CHUNK * 2, dtype=np.int16).tobytes()

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
            self.refresh_wave(c_id)
        elif self.waveSelect[c_id].currentIndex() in self.rule[var_id]:
            self.refresh_wave(c_id)

    def refresh_wave(self, c_id):
        self.idx[c_id] = 0
        self.wave_type[c_id] = self.waveSelect[c_id].currentIndex()
        self.sig[c_id] = getWave(
            self.wave_type[c_id],
            self.CHUNK,
            self.output_gain,
            self.RATE,
            self.freqInput[c_id].value(),
            self.ampInput[c_id].value(),
            self.dutyInput[c_id].value() / 100,
            self.offsetInput[c_id].value(),
            self.phiInput[c_id].value(),
            self.expInput[c_id].text(),
            self.fileInput[c_id].text(),
        )
        self.plot_fig(c_id)

    @pyqtSlot(int)
    def on_synchSelect_currentIndexChanged(self):
        if self.synchSelect.currentIndex() == 1:
            self.refresh_wave(0)
            self.refresh_wave(1)

    def plot_fig(self, c_id):
        self.fig[c_id].ax.cla()
        self.fig[c_id].set_ax()
        if type(self.sig[c_id]) == bool:
            self.fig[c_id].ax.plot([0, 1], [0.5, 0.5], c="r")
            self.sig[c_id] = np.zeros(self.CHUNK)
        elif self.wave_type[c_id] == 7:
            self.fig[c_id].ax.plot(
                np.linspace(0, 1, num=len(self.sig[c_id])),
                self.sig[c_id] / 2 + 0.5,
            )
        else:
            self.fig[c_id].ax.plot(
                np.linspace(0, 1, num=2 * len(self.sig[c_id])),
                np.tile((self.sig[c_id] / 2 + 0.5), 2),
            )
        self.fig[c_id].draw()

    def update_sig(self):
        for k in range(self.CHUNK):
            self.play_y[2 * k] = self.sig[0][self.idx[0]]
            self.play_y[2 * k + 1] = self.sig[1][self.idx[1]]
            self.idx = [(self.idx[i] + 1) % len(self.sig[i]) for i in [0, 1]]
        self.play_bytes = (self.play_y * 32768).astype(np.int16).tobytes()

    def reset(self):
        self.play_y = np.zeros(self.CHUNK * 2)
        self.play_bytes = np.zeros(self.CHUNK * 2, dtype=np.int16).tobytes()
        self.idx = [0, 0]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SignalGenerator()
    win.run()
    win.show()
    sys.exit(app.exec_())
