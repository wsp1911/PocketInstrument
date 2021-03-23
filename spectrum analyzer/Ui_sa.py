# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\Project\Python\PocketInstrument\analyzer\va.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys, os

sys.path.append(os.getcwd())

from PyQt5 import QtCore, QtGui, QtWidgets
from public.public import logSpinBox, doubleSlider


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.desktop = QtWidgets.QApplication.desktop()

        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        # self.height = self.screenRect.height()
        # self.width = self.screenRect.width()
        # WIDTH, HEIGHT = 1800, 1000
        WIDTH = int(0.9 * self.screenRect.width())
        HEIGHT = int(0.7 * self.screenRect.height())

        winW = 2 * WIDTH // 3
        sliderW, sliderH = 15, HEIGHT
        sliderX, sliderY = winW, 0

        sx = [i * sliderW + sliderX for i in range(4)]

        itemW, itemH = 100, 40
        btnW, btnH = itemW, 40
        labelW, labelH = itemW, itemH
        inputW, inputH = 150, itemH
        selectW, selectH = 150, itemH
        funcW, funcH = WIDTH - winW - 2 * marginL - 5 * sliderW, HEIGHT
        funcX, funcY = winW + 2 * marginL + 4 * sliderW, 0
        itemW = max([btnW, labelW, inputW])
        itemNX, itemNY = 4, 20
        itemdX = (funcW - labelW * 2 - inputW * 2) // (itemNX - 1)
        itemdY = (funcH - itemNY * itemH) // (itemNY - 1)
        x = [funcX + i * (itemW + itemdX) for i in range(itemNX)]
        x = [funcX, 0, 0, 0]
        x[1] = x[0] + labelW + itemdX
        x[2] = x[1] + inputW + itemdX
        x[3] = x[2] + labelW + itemdX

        y = [funcY + i * (itemH + itemdY) for i in range(itemNY)]

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(WIDTH, HEIGHT)
        MainWindow.setFont(QtGui.QFont("宋体", 14))
        MainWindow.setWindowTitle("示波器")

        # sliderStyleSheet =
        """
            QSlider::groove:vertical {
                background: red;
                position: absolute; /* absolutely position 4px from the left and right of the widget. setting margins on the widget should work too... */
                left: 4px; right: 4px;
            }

            QSlider::handle:vertical {
                height: 15px;
                background: #439cf4;
                margin: 0 -4px; /* expand outside the groove */
            }

            QSlider::add-page:vertical {
                background: #439cf4;
            }

            QSlider::sub-page:vertical {
                background: #cbcbcb;
            }
        """

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.FigQGB = QtWidgets.QGroupBox(self.centralwidget)
        self.FigQGB.setGeometry(QtCore.QRect(0, 0, winW, HEIGHT))
        self.FigQGB.setObjectName("FigQGB")

        self.CursorX, self.CursorY = [], []
        self.CursorX.append(doubleSlider(self.centralwidget))
        self.CursorX[0].setGeometry(QtCore.QRect(sx[0], sliderY, sliderW, sliderH))
        self.CursorX[0].setOrientation(QtCore.Qt.Vertical)
        self.CursorX[0].setObjectName("CursorX0")
        # self.CursorX[0].setStyleSheet(sliderStyleSheet)

        self.CursorX.append(doubleSlider(self.centralwidget))
        self.CursorX[1].setGeometry(QtCore.QRect(sx[1], sliderY, sliderW, sliderH))
        self.CursorX[1].setOrientation(QtCore.Qt.Vertical)
        self.CursorX[1].setObjectName("CursorX1")
        # self.CursorX[1].setStyleSheet(sliderStyleSheet)

        self.CursorY.append(doubleSlider(self.centralwidget))
        self.CursorY[0].setGeometry(QtCore.QRect(sx[2], sliderY, sliderW, sliderH))
        self.CursorY[0].setOrientation(QtCore.Qt.Vertical)
        self.CursorY[0].setObjectName("CursorY0")
        self.CursorY[0].setParameters(-10, 10, 1000)
        # self.CursorY[0].setStyleSheet(sliderStyleSheet)

        self.CursorY.append(doubleSlider(self.centralwidget))
        self.CursorY[1].setGeometry(QtCore.QRect(sx[3], sliderY, sliderW, sliderH))
        self.CursorY[1].setOrientation(QtCore.Qt.Vertical)
        self.CursorY[1].setObjectName("CursorY1")
        self.CursorY[1].setParameters(-10, 10, 1000)
        # self.CursorY[1].setStyleSheet(sliderStyleSheet)

        self.Trigger = doubleSlider(self.centralwidget)
        self.Trigger.setGeometry(
            QtCore.QRect(WIDTH - sliderW, sliderY, sliderW, sliderH)
        )
        self.Trigger.setOrientation(QtCore.Qt.Vertical)
        self.Trigger.setObjectName("Trigger")
        self.Trigger.setParameters(-10, 10, 1000)
        self.Trigger.setValue(0)

        self.RunButton = QtWidgets.QPushButton(self.centralwidget)
        self.RunButton.setGeometry(QtCore.QRect(x[-1], y[0], btnW, btnH))
        self.RunButton.setObjectName("RunButton")

        # 水平时基调整
        i, j = 0, 1
        self.tZoomLabel = QtWidgets.QLabel(self.centralwidget)
        self.tZoomLabel.setGeometry(QtCore.QRect(x[i], y[j], labelW, labelH))
        self.tZoomLabel.setObjectName("tZoomLabel")
        self.tZoomLabel.setText("时基")
        self.tZoomInput = logSpinBox(self.centralwidget)
        self.tZoomInput.setGeometry(QtCore.QRect(x[i + 1], y[j], inputW, inputH))
        self.tZoomInput.setObjectName("tZoomInput")
        self.tZoomInput.setParameters(mi=0.125, ma=10, step=0.5, decimal=3)

        # 显示选项
        i, j = 2, 1
        self.ModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.ModeSelect = QtWidgets.QComboBox(self.centralwidget)
        self.ModeLabel.setGeometry(QtCore.QRect(x[i], y[j], labelW, labelH))
        self.ModeLabel.setObjectName("ModeLabel")
        self.ModeLabel.setText("模式")
        self.ModeSelect.setGeometry(QtCore.QRect(x[i + 1], y[j], selectW, selectH))
        self.ModeSelect.setObjectName("Modeselect")
        self.ModeSelect.addItems(("水平", "XY", "时谱图"))

        # 测量面板
        i, j = 0, 2
        self.CursorLabel = QtWidgets.QLabel(self.centralwidget)
        self.CursorLabel.setGeometry(QtCore.QRect(x[i], y[j], labelW, labelH))
        self.CursorLabel.setObjectName("CursorLabel")
        self.CursorLabel.setText("光标源")
        self.CursorSource = QtWidgets.QComboBox(self.centralwidget)
        self.CursorSource.setGeometry(QtCore.QRect(x[i + 1], y[j], selectW, selectH))
        self.CursorSource.setObjectName("CursorSource")
        self.CursorSource.addItems(("1", "2"))

        # 触发设置
        i, j = 2, 2
        self.TriggerSourceLabel = QtWidgets.QLabel(self.centralwidget)
        self.TriggerSourceLabel.setGeometry(QtCore.QRect(x[i], y[j], labelW, labelH))
        self.TriggerSourceLabel.setObjectName("TriggerSourceLabel")
        self.TriggerSourceLabel.setText("触发源")
        self.TriggerSource = QtWidgets.QComboBox(self.centralwidget)
        self.TriggerSource.setGeometry(QtCore.QRect(x[i + 1], y[j], selectW, selectH))
        self.TriggerSource.setObjectName("TriggerSource")
        self.TriggerSource.addItems(("1", "2"))
        self.TriggerSlopeLabel = QtWidgets.QLabel(self.centralwidget)
        self.TriggerSlopeLabel.setGeometry(QtCore.QRect(x[i], y[j + 1], labelW, labelH))
        self.TriggerSlopeLabel.setObjectName("TriggerSlopeLabel")
        self.TriggerSlopeLabel.setText("边沿")
        self.TriggerSlopeSelect = QtWidgets.QComboBox(self.centralwidget)
        self.TriggerSlopeSelect.setGeometry(
            QtCore.QRect(x[i + 1], y[j + 1], selectW, selectH)
        )
        self.TriggerSlopeSelect.setObjectName("TriggerSlopeSelect")
        self.TriggerSlopeSelect.addItems(("上升", "下降"))

        # fft控制
        i, j = 0, 14
        self.fftLabel = QtWidgets.QLabel(self.centralwidget)
        self.fftLabel.setGeometry(QtCore.QRect(x[i], y[j], labelW, labelH))
        self.fftLabel.setObjectName("fftLabel")
        self.fftLabel.setText("FFT")

        self.fftChanLabel = QtWidgets.QLabel(self.centralwidget)
        self.fftChanLabel.setGeometry(QtCore.QRect(x[i], y[j + 1], labelW, labelH))
        self.fftChanLabel.setObjectName("fftChanLabel")
        self.fftChanLabel.setText("源")
        self.fftSource = QtWidgets.QComboBox(self.centralwidget)
        self.fftSource.setGeometry(QtCore.QRect(x[i + 1], y[j + 1], selectW, selectH))
        self.fftSource.setObjectName("fftSource")
        self.fftSource.addItems(("1", "2"))

        self.fftWinLabel = QtWidgets.QLabel(self.centralwidget)
        self.fftWinLabel.setGeometry(QtCore.QRect(x[i], y[j + 2], labelW, labelH))
        self.fftWinLabel.setObjectName("fftWinLabel")
        self.fftWinLabel.setText("窗类型")
        self.fftWinSelect = QtWidgets.QComboBox(self.centralwidget)
        self.fftWinSelect.setGeometry(
            QtCore.QRect(x[i + 1], y[j + 2], selectW, selectH)
        )
        self.fftWinSelect.setObjectName("fftWinSelect")
        self.fftWinSelect.addItems(("矩形窗", "汉明窗"))

        self.fftNLabel = QtWidgets.QLabel(self.centralwidget)
        self.fftNLabel.setGeometry(QtCore.QRect(x[i], y[j + 3], labelW, labelH))
        self.fftNLabel.setObjectName("fftNLabel")
        self.fftNLabel.setText("N")
        self.fftN = logSpinBox(self.centralwidget)
        self.fftN.setGeometry(QtCore.QRect(x[i + 1], y[j + 3], inputW, labelH))
        self.fftN.setDecimals(0)
        self.fftN.setRange(1, 16384)
        self.fftN.setSingleStep(2)
        self.fftN.setValue(4096)

        self.TSNLabel = QtWidgets.QLabel(self.centralwidget)
        self.TSNLabel.setGeometry(QtCore.QRect(x[i], y[j + 4], labelW, labelH))
        self.TSNLabel.setObjectName("TSNLabel")
        self.TSNLabel.setText("N")
        self.TSN = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.TSN.setGeometry(QtCore.QRect(x[i + 1], y[j + 4], inputW, labelH))
        self.TSN.setDecimals(0)
        self.TSN.setRange(1, 200)
        self.TSN.setSingleStep(1)
        self.TSN.setValue(100)

        self.fftRangeLabel = [
            QtWidgets.QLabel(self.centralwidget),
            QtWidgets.QLabel(self.centralwidget),
        ]
        self.fftRangeInput = [
            QtWidgets.QDoubleSpinBox(self.centralwidget),
            QtWidgets.QDoubleSpinBox(self.centralwidget),
        ]
        self.fftRangeLabel[0].setGeometry(
            QtCore.QRect(x[i + 2], y[j + 1], labelW, labelH)
        )
        self.fftRangeLabel[0].setObjectName("fftRangeLabel0")
        self.fftRangeLabel[0].setText("fmin")
        self.fftRangeInput[0].setGeometry(
            QtCore.QRect(x[i + 3], y[j + 1], inputW, inputH)
        )
        self.fftRangeInput[0].setObjectName("fftRangeInput0")
        self.fftRangeInput[0].setRange(0, 22050)
        self.fftRangeInput[0].setSingleStep(5)
        self.fftRangeInput[0].setValue(0)
        self.fftRangeLabel[1].setGeometry(
            QtCore.QRect(x[i + 2], y[j + 2], labelW, labelH)
        )
        self.fftRangeLabel[1].setObjectName("fftRangeLabel1")
        self.fftRangeLabel[1].setText("fmax")
        self.fftRangeInput[1].setGeometry(
            QtCore.QRect(x[i + 3], y[j + 2], inputW, inputH)
        )
        self.fftRangeInput[1].setObjectName("fftRangeInput1")
        self.fftRangeInput[1].setRange(0, 22050)
        self.fftRangeInput[1].setSingleStep(5)
        self.fftRangeInput[1].setValue(22050)

        self.fftCursorLabel = [
            QtWidgets.QLabel(self.centralwidget),
            QtWidgets.QLabel(self.centralwidget),
        ]
        self.fftCursorInput = [
            QtWidgets.QDoubleSpinBox(self.centralwidget),
            QtWidgets.QDoubleSpinBox(self.centralwidget),
        ]
        self.fftCursorLabel[0].setGeometry(
            QtCore.QRect(x[i + 2], y[j + 3], labelW, labelH)
        )
        self.fftCursorLabel[0].setObjectName("fftCursorLabel0")
        self.fftCursorLabel[0].setText("f1")
        self.fftCursorInput[0].setGeometry(
            QtCore.QRect(x[i + 3], y[j + 3], inputW, inputH)
        )
        self.fftCursorInput[0].setObjectName("fftCursorInput0")
        self.fftCursorInput[0].setRange(0, 22050)
        self.fftCursorInput[0].setSingleStep(1)
        self.fftCursorInput[0].setValue(0)
        self.fftCursorLabel[1].setGeometry(
            QtCore.QRect(x[i + 2], y[j + 4], labelW, labelH)
        )
        self.fftCursorLabel[1].setObjectName("fftCursorLabel1")
        self.fftCursorLabel[1].setText("f2")
        self.fftCursorInput[1].setGeometry(
            QtCore.QRect(x[i + 3], y[j + 4], inputW, inputH)
        )
        self.fftCursorInput[1].setObjectName("fftCursorInput1")
        self.fftCursorInput[1].setRange(0, 22050)
        self.fftCursorInput[1].setSingleStep(1)
        self.fftCursorInput[1].setValue(22050)

        # 通道控制
        (
            self.ChannelLabel,
            self.ZoomLabel,
            self.ZoomInput,
            self.OffsetLabel,
            self.OffsetInput,
        ) = ([], [], [], [], [])

        i, j = 0, 11
        self.ChannelLabel.append(QtWidgets.QLabel(self.centralwidget))
        self.ChannelLabel[0].setGeometry(QtCore.QRect(x[i], y[j], labelW, labelH))
        self.ChannelLabel[0].setObjectName("ChannelLabel_1")
        self.ChannelLabel[0].setText("通道1")

        self.ZoomLabel.append(QtWidgets.QLabel(self.centralwidget))
        self.ZoomLabel[0].setGeometry(QtCore.QRect(x[i], y[j + 1], labelW, labelH))
        self.ZoomLabel[0].setObjectName("ZoomLabel_1")
        self.ZoomLabel[0].setText("Zoom")

        self.ZoomInput.append(logSpinBox(self.centralwidget))
        self.ZoomInput[0].setGeometry(QtCore.QRect(x[i + 1], y[j + 1], inputW, inputH))
        self.ZoomInput[0].setObjectName("ZoomInput_1")
        self.ZoomInput[0].setParameters(mi=0.01, ma=20, step=0.5, decimal=3)

        self.OffsetLabel.append(QtWidgets.QLabel(self.centralwidget))
        self.OffsetLabel[0].setGeometry(QtCore.QRect(x[i], y[j + 2], labelW, labelH))
        self.OffsetLabel[0].setObjectName("OffsetLabel_1")
        self.OffsetLabel[0].setText("Offset")

        self.OffsetInput.append(QtWidgets.QDoubleSpinBox(self.centralwidget))
        self.OffsetInput[0].setGeometry(
            QtCore.QRect(x[i + 1], y[j + 2], inputW, inputH)
        )
        self.OffsetInput[0].setSingleStep(0.5)
        self.OffsetInput[0].setObjectName("OffsetInput_1")
        self.OffsetInput[0].setMinimum(-10)
        self.OffsetInput[0].setMaximum(10)

        i, j = 2, 11
        self.ChannelLabel.append(QtWidgets.QLabel(self.centralwidget))
        self.ChannelLabel[1].setGeometry(QtCore.QRect(x[i], y[j], labelW, labelH))
        self.ChannelLabel[1].setObjectName("ChannelLabel_2")
        self.ChannelLabel[1].setText("通道2")

        self.ZoomLabel.append(QtWidgets.QLabel(self.centralwidget))
        self.ZoomLabel[1].setGeometry(QtCore.QRect(x[i], y[j + 1], labelW, labelH))
        self.ZoomLabel[1].setObjectName("ZoomLabel_2")
        self.ZoomLabel[1].setText("Zoom")
        self.ZoomInput.append(logSpinBox(self.centralwidget))
        self.ZoomInput[1].setGeometry(QtCore.QRect(x[i + 1], y[j + 1], inputW, inputH))
        self.ZoomInput[1].setObjectName("ZoomInput_2")
        self.ZoomInput[1].setParameters(mi=0.01, ma=20, step=0.5, decimal=3)

        self.OffsetLabel.append(QtWidgets.QLabel(self.centralwidget))
        self.OffsetLabel[1].setGeometry(QtCore.QRect(x[i], y[j + 2], labelW, labelH))
        self.OffsetLabel[1].setObjectName("OffsetLabel_2")
        self.OffsetLabel[1].setText("Offset")
        self.OffsetInput.append(QtWidgets.QDoubleSpinBox(self.centralwidget))
        self.OffsetInput[1].setGeometry(
            QtCore.QRect(x[i + 1], y[j + 2], inputW, inputH)
        )
        self.OffsetInput[1].setSingleStep(0.5)
        self.OffsetInput[1].setObjectName("OffsetInput_2")
        self.OffsetInput[1].setMinimum(-10)
        self.OffsetInput[1].setMaximum(10)

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
        # self.PlotQGB.setTitle(_translate("MainWindow", "波形"))
        self.RunButton.setText(_translate("MainWindow", "Stop"))
        self.RunButton.setStyleSheet("background-color: red;")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
