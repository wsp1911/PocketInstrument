# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\Project\Python\PocketInstrument\analyzer\va.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys, os

sys.path.append(os.getcwd())
from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QGridLayout,
    QSizePolicy,
    QWidget,
    QPushButton,
    QLineEdit,
    QComboBox,
    QLabel,
    QDoubleSpinBox,
    QSpinBox,
    QMenuBar,
    QStatusBar,
    QToolBar,
    QCheckBox,
)
from PyQt5.QtGui import QFont
from public.public import logSpinBox, doubleSlider
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class plot_t(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        # new figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        super(FigureCanvas, self).__init__(self.fig)
        self.setParent(parent)

        # 主窗口
        pos = [0.02, 0, 0.92, 0.97]
        self.ax = self.fig.add_axes(pos)

        # 显示每格刻度
        upper_pos = [0, pos[3], 1, 1 - pos[3]]
        self.ax_upper = self.fig.add_axes(upper_pos)
        self.init_ax(self.ax_upper)

        # 显示GND
        left_pos = [0, 0, pos[0], pos[3]]
        self.ax_left = self.fig.add_axes(left_pos)
        self.init_ax(self.ax_left)

        # 显示测量数据
        right_pos = [
            pos[0] + pos[2],
            0,
            1 - pos[0] - pos[2],
            pos[3],
        ]
        self.ax_right = self.fig.add_axes(right_pos)
        self.init_ax(self.ax_right)

        # 两通道颜色
        self.c = ["#ffff00", "#00ff00"]

        font_c, font_size = "white", 12
        text_x = 0.05

        y = [0.05 * i for i in range(21)]
        self.fixed_text = {
            "1": self.ax_upper.text(0, 0, "1", c=self.c[0], fontsize=font_size),
            "2": self.ax_upper.text(0.3, 0, "2", c=self.c[1], fontsize=font_size),
            "t1": self.ax_right.text(
                text_x, y[19], "t1/ms", c=font_c, fontsize=font_size
            ),
            "t2": self.ax_right.text(
                text_x, y[17], "t2/ms", c=font_c, fontsize=font_size
            ),
            "Y1": self.ax_right.text(
                text_x, y[15], "Y1/V", c=font_c, fontsize=font_size
            ),
            "Y2": self.ax_right.text(
                text_x, y[13], "Y2/V", c=font_c, fontsize=font_size
            ),
            "dt": self.ax_right.text(
                text_x, y[11], r"$\Delta$t/ms", c=font_c, fontsize=font_size
            ),
            "1/dt": self.ax_right.text(
                text_x, y[9], "1/" + r"$\Delta$t/Hz", c=font_c, fontsize=font_size
            ),
            "dY": self.ax_right.text(
                text_x, y[7], r"$\Delta$Y/V", c=font_c, fontsize=font_size
            ),
        }

        self.data = {
            "1": self.ax_upper.text(0.02, 0, "0", fontsize=font_size),
            "2": self.ax_upper.text(0.32, 0, "0", fontsize=font_size),
            "t": self.ax_upper.text(0.8, 0, "0", fontsize=font_size),
            "t1": self.ax_right.text(
                1,
                y[18],
                "0",
                c=font_c,
                fontsize=font_size,
                horizontalalignment="right",
            ),
            "t2": self.ax_right.text(
                1,
                y[16],
                "0",
                c=font_c,
                fontsize=font_size,
                horizontalalignment="right",
            ),
            "Y1": self.ax_right.text(
                1, y[14], "0", c=font_c, fontsize=font_size, horizontalalignment="right"
            ),
            "Y2": self.ax_right.text(
                1, y[12], "0", c=font_c, fontsize=font_size, horizontalalignment="right"
            ),
            "dt": self.ax_right.text(
                1, y[10], "0", c=font_c, fontsize=font_size, horizontalalignment="right"
            ),
            "1/dt": self.ax_right.text(
                1, y[8], "0", c=font_c, fontsize=font_size, horizontalalignment="right"
            ),
            "dY": self.ax_right.text(
                1, y[6], "0", c=font_c, fontsize=font_size, horizontalalignment="right"
            ),
        }

        for i in range(2, 20, 2):
            self.ax_right.axhline(y=y[i], c="gray")

        # initial figure
        self.compute_initial_figure()

        # size policy
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def init_ax(self, ax):
        ax.set_xlim((0, 1))
        ax.set_ylim((0, 1))
        ax.set_xticks([])
        ax.set_yticks([])

    def compute_initial_figure(self):
        pass


class plot_f(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        # new figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        # 主窗口
        d1, d2, d = 0.05, 0.05, 0.06
        self.ax = self.fig.add_axes([d1, d2, 1 - 2 * d1 - d, 1 - 2 * d2])

        self.ax1 = self.fig.add_axes([1 - d, 0, d, 1])
        self.init_ax(self.ax1)

        # 两通道颜色
        self.c = ["#ffff00", "#00ff00"]

        font_c, font_size = "white", 12
        text_x = 0.05

        y1, y2, dy = 0.95, 0.9, 0.1
        self.fixed_text = {
            "f1": self.ax1.text(text_x, y1, "f1/Hz", c=font_c, fontsize=font_size),
            "f2": self.ax1.text(text_x, y1 - dy, "f2/Hz", c=font_c, fontsize=font_size),
            "Y1": self.ax1.text(
                text_x, y1 - 2 * dy, "Y1/dB", c=font_c, fontsize=font_size
            ),
            "Y2": self.ax1.text(
                text_x, y1 - 3 * dy, "Y2/dB", c=font_c, fontsize=font_size
            ),
            "df": self.ax1.text(
                text_x, y1 - 4 * dy, r"$\Delta$f/Hz", c=font_c, fontsize=font_size
            ),
            "dY": self.ax1.text(
                text_x, y1 - 5 * dy, r"$\Delta$Y/dB", c=font_c, fontsize=font_size
            ),
        }

        self.data = {
            "f1": self.ax1.text(
                1,
                y2,
                "0",
                c=font_c,
                fontsize=font_size,
                horizontalalignment="right",
            ),
            "f2": self.ax1.text(
                1,
                y2 - dy,
                "0",
                c=font_c,
                fontsize=font_size,
                horizontalalignment="right",
            ),
            "Y1": self.ax1.text(
                1,
                y2 - 2 * dy,
                "0",
                c=font_c,
                fontsize=font_size,
                horizontalalignment="right",
            ),
            "Y2": self.ax1.text(
                1,
                y2 - 3 * dy,
                "0",
                c=font_c,
                fontsize=font_size,
                horizontalalignment="right",
            ),
            "df": self.ax1.text(
                1,
                y2 - 4 * dy,
                "0",
                c=font_c,
                fontsize=font_size,
                horizontalalignment="right",
            ),
            "dY": self.ax1.text(
                1,
                y2 - 5 * dy,
                "0",
                c=font_c,
                fontsize=font_size,
                horizontalalignment="right",
            ),
        }

        for i in range(9):
            self.ax1.axhline(y=0.1 * (i + 1), c="gray")

        # initial figure
        self.compute_initial_figure()

        # size policy
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def init_ax(self, ax):
        ax.set_xlim((0, 1))
        ax.set_ylim((0, 1))
        ax.set_xticks([])
        ax.set_yticks([])

    def compute_initial_figure(self):
        pass


class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.desktop = QApplication.desktop()

        # 获取显示器分辨率大小
        # self.screenRect = self.desktop.screenGeometry()
        # WIDTH = int(0.9 * self.screenRect.width())
        # HEIGHT = int(0.9 * self.screenRect.height())

        self.screenRect = self.desktop.availableGeometry()
        WIDTH = int(0.9 * self.screenRect.width())
        HEIGHT = int(0.8 * self.screenRect.height())

        self.font_size = 9
        self.Font = QFont("等线", self.font_size)
        self.setObjectName("MainWindow")
        self.resize(WIDTH, HEIGHT)
        self.setFont(self.Font)
        self.setWindowTitle("示波器")
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        # self.menubar = QMenuBar()
        # self.menubar.setObjectName("menubar")
        # self.menu_file = self.menubar.addMenu("文件")
        # self.menu_func = self.menubar.addMenu("功能")
        # self.menu_set = self.menubar.addMenu("设置")
        # self.setMenuBar(self.menubar)

        # self.toolbar = QToolBar()
        self.toolbar = self.addToolBar("toolbar")
        self.toolbar.setObjectName("toolbar")
        self.toolbar.addAction("校准")
        self.toolbar.addAction("信号发生器")
        self.toolbar.addAction("波特图仪")

        self.FigQGB = [QGroupBox(self.centralwidget), QGroupBox(self.centralwidget)]
        self.FigQGB[0].setObjectName("FigQGB_0")
        # self.FigQGB[0].setTitle("t")
        self.FigQGB[1].setObjectName("FigQGB_1")
        # self.FigQGB[1].setTitle("f")
        self.HSliderQGB = QGroupBox(self.centralwidget)
        self.HSliderQGB.setObjectName("HSliderQGB")
        self.VSliderQGB = QGroupBox(self.centralwidget)
        self.VSliderQGB.setObjectName("HSliderQGB")
        self.CtrlQGB = QGroupBox(self.centralwidget)
        self.CtrlQGB.setObjectName("CtrlQGB")
        self.tFuncQGB = QGroupBox(self.centralwidget)
        self.tFuncQGB.setObjectName("tFuncQGB")
        self.tFuncQGB.setTitle("t")
        self.ChanQGB = []
        self.ChanQGB.append(QGroupBox(self.centralwidget))
        self.ChanQGB[0].setObjectName("ChanQGB_0")
        self.ChanQGB[0].setTitle("1")
        self.ChanQGB.append(QGroupBox(self.centralwidget))
        self.ChanQGB[1].setObjectName("ChanQGB_1")
        self.ChanQGB[1].setTitle("2")
        self.fFuncQGB = QGroupBox(self.centralwidget)
        self.fFuncQGB.setObjectName("fFuncQGB")
        self.fFuncQGB.setTitle("f")
        self.FileQGB = QGroupBox(self.centralwidget)
        self.FileQGB.setObjectName("FileQGB")
        self.FileQGB.setTitle("File")

        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.adjust_size()

        self.fig_t = plot_t(width=5, height=5, dpi=100)
        self.fig_f = plot_f(width=5, height=5, dpi=100)

        self.FigGrid = [QGridLayout(self.FigQGB[0]), QGridLayout(self.FigQGB[1])]
        self.FigGrid[0].setObjectName("FigGrid_0")
        self.FigGrid[0].addWidget(self.fig_t)
        self.FigGrid[1].setObjectName("FigGrid_1")
        self.FigGrid[1].addWidget(self.fig_f)

        self.CursorX = [doubleSlider(), doubleSlider()]
        self.CursorX[0].setObjectName("CursorX_0")
        self.CursorX[0].setOrientation(QtCore.Qt.Horizontal)
        self.CursorX[0].setFixedHeight(10)
        self.CursorX[1].setObjectName("CursorX_1")
        self.CursorX[1].setOrientation(QtCore.Qt.Horizontal)
        self.CursorX[1].setFixedHeight(10)
        self.CursorX[1].setValue(1)

        self.HSliderGrid = QHBoxLayout(self.HSliderQGB)
        self.HSliderGrid.setObjectName("HSliderGrid")
        self.HSliderGrid.addWidget(self.CursorX[0])
        self.HSliderGrid.addWidget(self.CursorX[1])

        self.CursorY = [doubleSlider(), doubleSlider()]
        self.CursorY[0].setObjectName("CursorY_0")
        self.CursorY[0].setOrientation(QtCore.Qt.Vertical)
        self.CursorY[0].setFixedWidth(10)
        self.CursorY[1].setObjectName("CursorY_1")
        self.CursorY[1].setOrientation(QtCore.Qt.Vertical)
        self.CursorY[1].setFixedWidth(10)
        self.CursorY[1].setValue(1)

        self.VSliderGrid = QVBoxLayout(self.VSliderQGB)
        self.VSliderGrid.setObjectName("VSliderGrid")
        self.VSliderGrid.addWidget(self.CursorY[1])
        self.VSliderGrid.addWidget(self.CursorY[0])
        # self.VSliderGrid.addWidget(self.Trigger)

        self.RunButton = QPushButton()
        self.RunButton.setObjectName("RunButton")
        self.RunButton.setText("Run")
        # self.RunButton.setStyleSheet("background-color: green;")
        # self.RunButton.setFont(self.Font)

        self.ChannelLabel = QLabel("通道")
        self.ChannelLabel.setObjectName("ChannelLabel")
        self.Channel = QComboBox()
        self.Channel.setObjectName("Channel")
        self.Channel.addItems(("1 and 2", "1", "2", "XY"))

        self.CursorTargetLabel = QLabel("光标作用于")
        self.CursorTargetLabel.setObjectName("CursorTargetLabel")
        self.CursorTarget = QComboBox()
        self.CursorTarget.setObjectName("CursorTarget")
        self.CursorTarget.addItems(("波形", "频谱"))

        self.CtrlGrid = QGridLayout(self.CtrlQGB)
        self.CtrlGrid.setObjectName("CtrlGrid")
        self.CtrlGrid.addWidget(self.RunButton, 0, 1)
        self.CtrlGrid.addWidget(self.ChannelLabel, 1, 0)
        self.CtrlGrid.addWidget(self.Channel, 1, 1)
        self.CtrlGrid.addWidget(self.CursorTargetLabel, 2, 0)
        self.CtrlGrid.addWidget(self.CursorTarget, 2, 1)

        # 水平时基调整
        self.tZoomLabel = QLabel("zoom")
        self.tZoomLabel.setObjectName("tZoomLabel")
        self.tZoom = logSpinBox()
        self.tZoom.setObjectName("tZoom")
        self.tZoom.setParameters(mi=1, ma=128, val=16, step=2, decimal=0)

        # 测量面板
        self.MeasLabel = QLabel("测量")
        self.MeasLabel.setObjectName("MeasLabel")
        self.MeasChan = QComboBox()
        self.MeasChan.setObjectName("MeasChan")
        self.MeasChan.addItems(("1", "2"))

        self.CursorCB = QCheckBox("Cursor")
        self.CursorCB.setObjectName("CursorCB")

        self.tFuncGrid = QGridLayout(self.tFuncQGB)
        self.tFuncGrid.setObjectName("tFuncGrid")
        self.tFuncGrid.addWidget(self.tZoomLabel, 0, 0, 1, 2)
        self.tFuncGrid.addWidget(self.tZoom, 0, 2, 1, 2)
        self.tFuncGrid.addWidget(self.CursorCB, 1, 0)
        self.tFuncGrid.addWidget(self.MeasLabel, 1, 2)
        self.tFuncGrid.addWidget(self.MeasChan, 1, 3)

        # 通道控制
        self.Trigger = [doubleSlider(), doubleSlider()]
        self.Trigger[0].setParameters(-10, 10, 2000)
        self.Trigger[0].setValue(0)
        self.Trigger[1].setParameters(-10, 10, 2000)
        self.Trigger[1].setValue(0)
        self.Trigger[0].setObjectName("Trigger_0")
        self.Trigger[0].setOrientation(QtCore.Qt.Vertical)
        self.Trigger[0].setFixedWidth(10)
        self.Trigger[1].setObjectName("Trigger_1")
        self.Trigger[1].setOrientation(QtCore.Qt.Vertical)
        self.Trigger[1].setFixedWidth(10)

        self.tYZoomLabel = [QLabel("zoom"), QLabel("zoom")]
        self.tYZoom = [logSpinBox(), logSpinBox()]
        self.OffsetLabel = [QLabel("offset"), QLabel("offset")]
        self.Offset = [QDoubleSpinBox(), QDoubleSpinBox()]

        self.tYZoomLabel[0].setObjectName("tYZoomLabel_0")
        self.tYZoomLabel[1].setObjectName("tYZoomLabel_1")

        self.tYZoom[0].setObjectName("tYZoom_0")
        self.tYZoom[0].setParameters(mi=0.1, ma=20, val=1, step=2, decimal=2)
        self.tYZoom[1].setObjectName("tYZoom_1")
        self.tYZoom[1].setParameters(mi=0.1, ma=20, val=1, step=2, decimal=2)

        self.OffsetLabel[0].setObjectName("OffsetLabel_0")
        self.OffsetLabel[1].setObjectName("OffsetLabel_1")

        self.Offset[0].setSingleStep(0.5)
        self.Offset[0].setObjectName("Offset_0")
        self.Offset[0].setMinimum(-10)
        self.Offset[0].setMaximum(10)
        self.Offset[1].setSingleStep(0.5)
        self.Offset[1].setObjectName("Offset_1")
        self.Offset[1].setMinimum(-10)
        self.Offset[1].setMaximum(10)

        # 触发设置
        self.TriggerCB = [QCheckBox("Trig"), QCheckBox("Trig")]
        self.TriggerCB[0].setObjectName("TriggerCB_0")
        self.TriggerCB[1].setObjectName("TriggerCB_1")
        self.TriggerCB[0].setCheckState(QtCore.Qt.Checked)
        self.TriggerCB[1].setCheckState(QtCore.Qt.Checked)
        self.TriggerSlopeLabel = [QLabel("边沿"), QLabel("边沿")]
        self.TriggerSlopeLabel[0].setObjectName("TriggerSlopeLabel_0")
        self.TriggerSlopeLabel[1].setObjectName("TriggerSlopeLabel_1")
        self.TriggerSlope = [QComboBox(), QComboBox()]
        self.TriggerSlope[0].setObjectName("TriggerSlope_0")
        self.TriggerSlope[0].addItems(("↑", "↓"))
        self.TriggerSlope[1].setObjectName("TriggerSlope_1")
        self.TriggerSlope[1].addItems(("↑", "↓"))

        self.ChanGrid = [QGridLayout(self.ChanQGB[0]), QGridLayout(self.ChanQGB[1])]
        self.ChanGrid[0].setObjectName("ChanGrid_0")
        self.ChanGrid[0].addWidget(self.Trigger[0], 0, 0, 4, 1)
        self.ChanGrid[0].addWidget(self.tYZoomLabel[0], 0, 1)
        self.ChanGrid[0].addWidget(self.tYZoom[0], 0, 2)
        self.ChanGrid[0].addWidget(self.OffsetLabel[0], 1, 1)
        self.ChanGrid[0].addWidget(self.Offset[0], 1, 2)
        self.ChanGrid[0].addWidget(self.TriggerCB[0], 2, 1)
        self.ChanGrid[0].addWidget(self.TriggerSlopeLabel[0], 3, 1)
        self.ChanGrid[0].addWidget(self.TriggerSlope[0], 3, 2)
        self.ChanGrid[1].setObjectName("ChanGrid_1")
        self.ChanGrid[1].addWidget(self.Trigger[1], 0, 0, 4, 1)
        self.ChanGrid[1].addWidget(self.tYZoomLabel[1], 0, 1)
        self.ChanGrid[1].addWidget(self.tYZoom[1], 0, 2)
        self.ChanGrid[1].addWidget(self.OffsetLabel[1], 1, 1)
        self.ChanGrid[1].addWidget(self.Offset[1], 1, 2)
        self.ChanGrid[1].addWidget(self.TriggerCB[1], 2, 1)
        self.ChanGrid[1].addWidget(self.TriggerSlopeLabel[1], 3, 1)
        self.ChanGrid[1].addWidget(self.TriggerSlope[1], 3, 2)

        self.fLogCB = QCheckBox("f log")
        self.fLogCB.setObjectName("fLogCB")
        self.ALogCB = QCheckBox("A log")
        self.ALogCB.setObjectName("ALogCB")
        self.ALogCB.setCheckState(QtCore.Qt.Checked)
        self.fCursorCB = QCheckBox("Cursor")
        self.fCursorCB.setObjectName("fCursorCB")

        self.WinTypeLabel = QLabel("窗类型")
        self.WinTypeLabel.setObjectName("WinTypeLabel")
        self.WinType = QComboBox()
        self.WinType.setObjectName("WinType")
        self.WinType.addItems(("Hanning", "Hamming", "Blackman", "Bartlete", "Rect"))

        self.fftNLabel = QLabel("N")
        self.fftNLabel.setObjectName("fftNLabel")
        self.fftN = logSpinBox()
        self.fftN.setObjectName("fftN")
        self.fftN.setParameters(mi=128, ma=32768, val=1024, step=2, decimal=0)
        self.fftN.setValue(16384)

        self.fZoomLabel = QLabel("zoom")
        self.fZoomLabel.setObjectName("fZoomLabel")
        self.fZoom = logSpinBox()
        self.fZoom.setObjectName("fZoom")
        self.fZoom.setParameters(mi=1, ma=128, val=1, step=2, decimal=0)

        self.fYLimLabel = [QLabel("Ymin"), QLabel("Ymax")]
        self.fYLimLabel[0].setObjectName("fYLimLabel_0")
        self.fYLimLabel[1].setObjectName("fYLimLabel_1")

        self.fYLim = [QDoubleSpinBox(), QDoubleSpinBox()]
        self.fYLim[0].setObjectName("fYLim_0")
        self.fYLim[1].setObjectName("fYLim_1")
        self.fYLim[0].setRange(-120, 20)
        self.fYLim[0].setSingleStep(5)
        self.fYLim[0].setValue(-120)
        self.fYLim[1].setRange(-120, 20)
        self.fYLim[1].setSingleStep(5)
        self.fYLim[1].setValue(20)

        self.fPos = doubleSlider()
        self.fPos.setObjectName("fPos")
        self.fPos.setOrientation(QtCore.Qt.Horizontal)
        self.fPos.setFixedHeight(10)

        self.fFuncGrid = QGridLayout(self.fFuncQGB)
        self.fFuncGrid.setObjectName("FuncGrid")
        self.fFuncGrid.addWidget(self.WinTypeLabel, 0, 0, 1, 2)
        self.fFuncGrid.addWidget(self.WinType, 0, 2, 1, 2)
        self.fFuncGrid.addWidget(self.fftNLabel, 1, 0, 1, 2)
        self.fFuncGrid.addWidget(self.fftN, 1, 2, 1, 2)
        self.fFuncGrid.addWidget(self.fCursorCB, 2, 0)
        self.fFuncGrid.addWidget(self.fLogCB, 2, 2)
        self.fFuncGrid.addWidget(self.ALogCB, 2, 3)
        self.fFuncGrid.addWidget(self.fZoomLabel, 3, 0, 1, 2)
        self.fFuncGrid.addWidget(self.fZoom, 3, 2, 1, 2)
        self.fFuncGrid.addWidget(self.fYLimLabel[0], 4, 0)
        self.fFuncGrid.addWidget(self.fYLim[0], 4, 1)
        self.fFuncGrid.addWidget(self.fYLimLabel[1], 4, 2)
        self.fFuncGrid.addWidget(self.fYLim[1], 4, 3)
        self.fFuncGrid.addWidget(self.fPos, 5, 0, 1, 4)

        self.filename = QLineEdit()
        self.filename.setObjectName("filename")

        self.PicFormat = QComboBox()
        self.PicFormat.setObjectName("PicFormat")
        self.PicFormat.addItems((".png", ".jpg"))
        self.PicSaveButton = QPushButton(text="保存图片")
        self.PicSaveButton.setObjectName("PicSaveButton")

        self.DataFormat = QComboBox()
        self.DataFormat.setObjectName("DataFormat")
        self.DataFormat.addItems((".npy", ".mat", ".wav"))
        self.DataSaveButton = QPushButton(text="保存数据")
        self.DataSaveButton.setObjectName("DataSaveButton")

        self.RecordFormat = QComboBox()
        self.RecordFormat.setObjectName("RecordFormat")
        self.RecordFormat.addItems((".npy", ".mat", ".wav"))
        self.RecordButton = QPushButton(text="开始录音")
        self.RecordButton.setObjectName("RecordButton")

        self.FileGrid = QGridLayout(self.FileQGB)
        self.FileGrid.setObjectName("FileGrid")
        # self.FileGrid.setAlignment(QtCore.Qt.AlignTop)
        # self.FileGrid.setRowStretch(0, 1)
        self.FileGrid.addWidget(self.filename, 0, 0, 1, 2)
        self.FileGrid.addWidget(self.PicFormat, 1, 0)
        self.FileGrid.addWidget(self.PicSaveButton, 1, 1)
        self.FileGrid.addWidget(self.DataFormat, 2, 0)
        self.FileGrid.addWidget(self.DataSaveButton, 2, 1)
        self.FileGrid.addWidget(self.RecordFormat, 3, 0)
        self.FileGrid.addWidget(self.RecordButton, 3, 1)

        self.setCentralWidget(self.centralwidget)

        # self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_size()

    def adjust_size(self):
        WIDTH, HEIGHT = self.width(), self.height()
        # toolH, statusH = 30, 30
        toolH = self.toolbar.geometry().height()
        statusH = self.statusbar.geometry().height()
        self.statusbar.showMessage(str(WIDTH) + " " + str(HEIGHT))
        sliderD = 40
        winY = 0
        winW, winH = int(WIDTH * 0.8) - sliderD, HEIGHT - sliderD - toolH - statusH
        rowN = 19
        rowH = (winH + sliderD) // rowN
        ctrlX, ctrlW = winW + sliderD, WIDTH - winW - sliderD
        ctrlY = 0
        ctrlH, tFuncH, chanH, fFuncH = (
            3 * rowH,
            2 * rowH,
            4 * rowH,
            6 * rowH,
        )
        tFuncY = ctrlY + ctrlH
        chanY = tFuncY + tFuncH
        fFuncY = chanY + chanH
        fileY = fFuncY + fFuncH
        fileH = winH + sliderD - ctrlH - tFuncH - chanH - fFuncH

        # self.toolbar.setGeometry(QRect(0, 0, WIDTH, toolH))
        self.FigQGB[0].setGeometry(QRect(0, winY, winW, winH // 2))
        self.FigQGB[1].setGeometry(QRect(0, winY + winH // 2, winW, winH // 2))
        self.HSliderQGB.setGeometry(QRect(0, winH + winY, winW, sliderD))
        self.VSliderQGB.setGeometry(QRect(winW, winY, sliderD, winH))
        self.CtrlQGB.setGeometry(QRect(ctrlX, ctrlY, ctrlW, ctrlH))
        self.tFuncQGB.setGeometry(QRect(ctrlX, tFuncY, ctrlW, tFuncH))
        self.ChanQGB[0].setGeometry(QRect(ctrlX, chanY, ctrlW // 2, chanH))
        self.ChanQGB[1].setGeometry(QRect(ctrlX + ctrlW // 2, chanY, ctrlW // 2, chanH))
        self.fFuncQGB.setGeometry(QRect(ctrlX, fFuncY, ctrlW, fFuncH))
        self.FileQGB.setGeometry(QRect(ctrlX, fileY, ctrlW, fileH))
        # self.statusbar.setGeometry(QRect(0, winY + winH + sliderD, WIDTH, statusH))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
