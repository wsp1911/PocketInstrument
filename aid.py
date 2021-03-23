# -*- coding: utf-8 -*-
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt5.QtCore import pyqtSlot
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import sys, time


class Myplot(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        # new figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        d = 0.05
        self.ax = self.fig.add_axes([d, d, 1 - 2 * d, 1 - 2 * d])

        # initial figure
        self.compute_initial_figure()

        # size policy
        FigureCanvas.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        FigureCanvas.updateGeometry(self)

    def set_ax(self):
        d = 0.03
        self.ax.set_xlim((-d, 1 + d))
        self.ax.set_ylim((-d, 1 + d))
        self.ax.set_xticks([])
        self.ax.set_yticks([])

    def compute_initial_figure(self):
        pass


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        W, H = 1600, 1200
        MainWindow.resize(W, H)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.fig = Myplot(width=5, height=5, dpi=100)

        self.QGB = QtWidgets.QGroupBox(self.centralwidget)
        self.QGB.setGeometry(QtCore.QRect(0, 0, W, H))

        self.grid = QtWidgets.QGridLayout(self.QGB)
        self.grid.addWidget(self.fig)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.play()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "test"))

    def play(self):
        fs = 44100
        f = 1000
        t = np.arange(0, 1, 1 / fs)
        frames, N = 100, 1024
        self.im = np.zeros((frames, N))
        for i in range(frames):
            f += 5
            x = np.sin(2 * np.pi * f * t)
            X = np.fft.fft(x, N)
            X_dB = 20 * np.log10(np.abs(X))
            self.im[frames - i - 1, :] = X_dB
        self.fig.ax.imshow(self.im)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":
#     t = np.arange(0, 2 * np.pi, 0.001)
#     x = 16 * np.sin(t) ** 3 / 16
#     y = (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)) / 16
#     plt.plot(x, y)
#     plt.axis("equal")
#     plt.axis("auto")
#     plt.xlim((-10, 10))
#     plt.show()
