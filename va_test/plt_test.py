import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt5.QtCore import pyqtSlot
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import sys, time
import threading

matplotlib.use("Qt5Agg")


class Myplot(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        # new figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        self.ax1 = self.fig.add_axes([0.03, 0.3, 0.85, 0.6])
        self.ax2 = self.fig.add_axes([0.03, 0, 0.85, 0.3])

        self.text = self.ax2.text(0, 1, "Hello world", c="#00ff00")

        self.ax1.axis("off")

        # initial figure
        self.compute_initial_figure()

        # size policy
        FigureCanvas.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # self.desktop = QtWidgets.QApplication.desktop()

        # 获取显示器分辨率大小
        # self.screenRect = self.desktop.screenGeometry()
        WIDTH, HEIGHT = 1600, 1000
        # WIDTH = int(0.9 * self.screenRect.width())
        # HEIGHT = int(0.9 * self.screenRect.height())

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(WIDTH, HEIGHT)
        MainWindow.setFont(QtGui.QFont("宋体", 14))
        MainWindow.setWindowTitle("示波器")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.TimeQGB = QtWidgets.QGroupBox(self.centralwidget)
        self.TimeQGB.setGeometry(QtCore.QRect(0, 0, WIDTH, HEIGHT))
        self.TimeQGB.setObjectName("TimeQGB")

        self.fig = Myplot()

        self.gridlayout1 = QGridLayout(self.TimeQGB)
        self.gridlayout1.addWidget(self.fig)

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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "示波器"))

    def run(self):
        i = 0
        while True:
            t = np.linspace(0, 10, 1000)
            phi = np.random.randint(1000) / 1000 * np.pi
            data = np.sin(2 * np.pi * 500 * t + phi)
            self.fig.ax1.clear()

            self.fig.ax1.plot(t, data)

            self.fig.ax1.set_xlim(0, 10)
            self.fig.ax1.set_ylim(-2, 2)
            # self.fig.ax1.axis("off")
            # self.fig.ax1.set_yticks([])
            self.fig.ax1.axes.xaxis.set_visible(False)
            self.fig.ax1.grid(True)
            self.fig.ax2.set_xlim(0, 10)
            self.fig.ax2.set_ylim(0, 2)

            self.fig.text.set_text(str(i))
            i += 1
            self.fig.draw()
            time.sleep(2)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    t1 = threading.Thread(target=ui.run)
    t1.start()
    sys.exit(app.exec_())
