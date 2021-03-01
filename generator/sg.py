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

from Ui_sg import Ui_MainWindow
from sigGenerate import getWave

# import wave
from pyaudio import PyAudio, paInt16

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


class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        self.setupUi(self)

        self.RUNNING = False
        self.REFRESH = False
        self.fs = 44100

        self.connect()

    def refreshWave(self):
        self.REFRESH = True

    def connect(self):
        self.waveSelect.currentIndexChanged.connect(self.refreshWave)
        self.freqInput.valueChanged.connect(self.refreshWave)
        self.ampInput.valueChanged.connect(self.refreshWave)
        self.offsetInput.valueChanged.connect(self.refreshWave)
        self.dutyInput.valueChanged.connect(self.refreshWave)
        self.phiInput.valueChanged.connect(self.refreshWave)
        self.waveSelect_2.currentIndexChanged.connect(self.refreshWave)
        self.freqInput_2.valueChanged.connect(self.refreshWave)
        self.ampInput_2.valueChanged.connect(self.refreshWave)
        self.offsetInput_2.valueChanged.connect(self.refreshWave)
        self.dutyInput_2.valueChanged.connect(self.refreshWave)
        self.phiInput_2.valueChanged.connect(self.refreshWave)

    def play(self):
        pa = PyAudio()
        stream = pa.open(
            format=paInt16,
            channels=2,
            rate=44100,
            output=True,
        )
        while True:
            y0 = getWave(
                self.waveSelect.currentIndex(),
                self.fs,
                self.freqInput.value(),
                self.ampInput.value(),
                self.dutyInput.value() / 100,
                self.offsetInput.value(),
                self.phiInput.value(),
            )
            y1 = getWave(
                self.waveSelect_2.currentIndex(),
                self.fs,
                self.freqInput_2.value(),
                self.ampInput_2.value(),
                self.dutyInput_2.value() / 100,
                self.offsetInput_2.value(),
                self.phiInput_2.value(),
            )

            if y0 is 0 and y1 is 0:
                continue
            elif y0 is 0:
                y = np.zeros(len(y1) * 2)
                for i in range(len(y1)):
                    y[2 * i] = 0
                    y[2 * i + 1] = y1[i]
                y_bytes = (y * 32768).astype(np.int16).tobytes()
                while True:
                    stream.write(y_bytes)
                    if self.REFRESH:
                        self.REFRESH = False
                        break
            elif y1 is 0:
                y = np.zeros(len(y0) * 2)
                for i in range(len(y0)):
                    y[2 * i] = y0[i]
                    y[2 * i + 1] = 0
                y_bytes = (y * 32768).astype(np.int16).tobytes()
                while True:
                    stream.write(y_bytes)
                    if self.REFRESH:
                        self.REFRESH = False
                        break
            else:
                L0, L1 = len(y0), len(y1)
                if L0 < L1:
                    y = np.zeros(2 * L1)
                    for i in range(L1):
                        y[2 * i + 1] = y1[i]
                    j = 0
                    while True:
                        for i in range(L1):
                            y[2 * i] = y0[j]
                            j = (j + 1) % L0
                        y_bytes = (y * 32768).astype(np.int16).tobytes()
                        stream.write(y_bytes)
                        if self.REFRESH:
                            self.REFRESH = False
                            break
                elif L0 > L1:
                    y = np.zeros(2 * L0)
                    for i in range(L0):
                        y[2 * i] = y0[i]
                    j = 0
                    while True:
                        for i in range(L0):
                            y[2 * i + 1] = y1[j]
                            j = (j + 1) % L1
                        y_bytes = (y * 32768).astype(np.int16).tobytes()
                        stream.write(y_bytes)
                        if self.REFRESH:
                            self.REFRESH = False
                            break
                else:
                    y = np.zeros(2 * L0)
                    for i in range(L0):
                        y[2 * i] = y0[i]
                        y[2 * i + 1] = y1[i]
                    y_bytes = (y * 32768).astype(np.int16).tobytes()
                    while True:
                        stream.write(y_bytes)
                        if self.REFRESH:
                            self.REFRESH = False
                            break
        stream.stop_stream()
        stream.close()  # 关闭
        pa.terminate()  # 终结


# @pyqtSlot()
# def on_RunButton_clicked(self):
#     if self.RUNNING:
#         self.RunButton.setText("Run")
#         self.RunButton.setStyleSheet("background-color: green;")
#     else:
#         self.RunButton.setText("Stop")
#         self.RunButton.setStyleSheet("background-color: red;")
#     self.RunButton.setFont(QtGui.QFont("宋体", 14))
#     self.RUNNING = not self.RUNNING


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    t1 = threading.Thread(target=win.play)
    t1.start()
    sys.exit(app.exec_())
