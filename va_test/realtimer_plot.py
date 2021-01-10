# -*- coding: utf-8 -*-

"""
Module: plot data realtime.
Created on 2020/07/12 by Blog Author VERtiCaL at SSRF
"""

import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QMainWindow, QGridLayout
from PyQt5.QtCore import QTimer, pyqtSlot, QThread
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import sys, random, time, os, re
from Ui_realtimer_plot import Ui_MainWindow


# class Myplot for plotting with matplotlib
class Myplot(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        # normalized for 中文显示和负号
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False

        # new figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # activate figure window
        # super(Plot_dynamic,self).__init__(self.fig)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        # self.fig.canvas.mpl_connect('button_press_event', self)
        # sub plot by self.axes
        self.axes = self.fig.add_subplot(111)
        # initial figure
        self.compute_initial_figure()

        # size policy
        FigureCanvas.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


# class for plotting a specific figure static or dynamic
class static_fig(Myplot):
    def __init__(self, *args, **kwargs):
        Myplot.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        x = np.linspace(0, 2 * np.pi, 100)
        y = x * np.sin(x)
        self.axes.plot(x, y)
        self.axes.set_title("signals")
        self.axes.set_xlabel("delay(s)")
        self.axes.set_ylabel("counts")


class dynamic_fig(Myplot):
    def __init__(self, *args, **kwargs):
        Myplot.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        counts = [1, 10]
        delay_t = [0, 1]
        self.axes.plot(delay_t, counts, "-ob")
        self.axes.set_title("signals")
        self.axes.set_xlabel("delay(s)")
        self.axes.set_ylabel("counts")


# class for the application window
class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        self.setupUi(self)
        # ^O^ static_fig can changed to any other function
        # self.fig1=static_fig(width=5, height=4, dpi=100)
        self.fig1 = static_fig(width=5, height=3, dpi=72)
        self.fig2 = dynamic_fig(width=5, height=3, dpi=72)
        # add NavigationToolbar in the figure (widgets)
        self.fig_ntb1 = NavigationToolbar(self.fig1, self)
        self.fig_ntb2 = NavigationToolbar(self.fig2, self)
        # self.Start_plot.clicked.connect(self.plot_cos)
        # add the static_fig in the Plot box
        self.gridlayout1 = QGridLayout(self.Plot_static)
        self.gridlayout1.addWidget(self.fig1)
        self.gridlayout1.addWidget(self.fig_ntb1)
        # add the dynamic_fig in the Plot box
        self.gridlayout2 = QGridLayout(self.Plot_dynamic)
        self.gridlayout2.addWidget(self.fig2)
        self.gridlayout2.addWidget(self.fig_ntb2)
        # initialized flags for static/dynamic plot: on is 1,off is 0
        self._timer = QTimer(self)
        self._t = 1
        self._counts = []
        self._delay_t = []
        self._Static_on = 0
        self._update_on = 0

    @pyqtSlot()
    def on_Static_plot_clicked(self):
        self.plot_cos()
        self._Static_on = 1
        # self.Start_plot.setEnabled(False)

    global nc
    nc = 1

    def plot_cos(self):
        # print('nc=%d\n' %self.nc)
        global nc
        nc += 1
        self.fig1.axes.cla()
        self.t = np.arange(0, 15, 0.1)
        self.y = 2 * nc * self.t - self.t * np.cos(self.t / 2 / np.pi * 1000)
        self.fig1.axes.plot(self.t, self.y)
        self.fig1.axes.set_title("signals", fontsize=18, color="c")
        self.fig1.axes.set_xlabel("delay(s)", fontsize=18, color="c")
        self.fig1.axes.set_ylabel("counts", fontsize=18, color="c")
        self.fig1.draw()

    @pyqtSlot()
    def on_dynamic_plot_clicked(self):
        print("start dynamic ploting")
        self.Static_plot.setEnabled(False)
        self.dynamic_plot.setEnabled(False)
        # start update figure every 1s; flag "update_on" : 1 is on and 0 is Off
        self._update_on = 1
        self._timer.timeout.connect(self.update_fig)
        self._timer.start(1000)  # plot after 1s delay

    def update_fig(self):
        self._t += 1
        print(self._t)
        self._delay_t.append(self._t)
        print(self._delay_t)
        # new_counts=random.randint(100,900)
        new_counts = 2 * self._t - self._t * np.cos(self._t / 2 / np.pi * 1000)
        self._counts.append(new_counts)
        print(self._counts)
        self.fig2.axes.cla()
        self.fig2.axes.plot(self._delay_t, self._counts, "-ob")
        self.fig2.axes.set_title("signals", fontsize=18, color="c")
        self.fig2.axes.set_xlabel("delay(s)", fontsize=18, color="c")
        self.fig2.axes.set_ylabel("counts", fontsize=18, color="c")
        self.fig2.draw()

    @pyqtSlot()
    def on_End_plot_clicked(self):
        if self._update_on == 1:
            self._update_on = 0
            self._timer.timeout.disconnect(self.update_fig)
            self.dynamic_plot.setEnabled(True)
        else:
            pass

    @pyqtSlot()
    def on_Erase_plot_clicked(self):
        self.fig1.axes.cla()
        self.fig1.draw()
        self.fig2.axes.cla()
        self.fig2.draw()
        if self._update_on == 1:
            self._update_on = 0
            self._delay_t = []
            self._counts = []
            self.fig2.axes.cla()
            self.fig2.draw()
            self._timer.timeout.disconnect(self.update_fig)
            self.dynamic_plot.setEnabled(True)
        else:
            pass
        self.Static_plot.setEnabled(True)
        # self.Erase_plot.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec_())
