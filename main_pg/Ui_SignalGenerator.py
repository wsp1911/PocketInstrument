# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg


class my_plot_widget(pg.PlotWidget):
    def __init__(self, parent=None, pen="w"):
        super(my_plot_widget, self).__init__(parent)

        self.curve = self.plot(pen=pen)
        self.setYRange(-10, 10)
        self.showAxis("right")


class Ui_SignalGenerator(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_SignalGenerator, self).__init__(parent=parent)

        WIDTH, HEIGHT = 1200, 800
        dispW, dispH = (WIDTH - 200) // 2, 200
        funcW, funcH = WIDTH - (WIDTH - 2 * dispW) // 2, HEIGHT - dispH - 100
        x, y = (WIDTH - funcW) // 2, (HEIGHT - funcH - dispH) * 2 // 3 + dispH
        x2 = WIDTH // 2 + x

        self.setObjectName("sg_MainWindow")
        self.resize(WIDTH, HEIGHT)
        self.setFont(QtGui.QFont("等线", 9))
        self.setWindowTitle("信号发生器")

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.FigQGB = [
            QtWidgets.QGroupBox(self.centralwidget),
            QtWidgets.QGroupBox(self.centralwidget),
        ]
        self.FigQGB[0].setGeometry(QtCore.QRect(x, (y - dispH) // 2, dispW, dispH))
        self.FigQGB[0].setObjectName("FigQGB_0")

        self.FigQGB[1].setGeometry(QtCore.QRect(x2, (y - dispH) // 2, dispW, dispH))
        self.FigQGB[1].setObjectName("FigQGB_1")

        self.pw = [my_plot_widget(pen="g"), my_plot_widget(pen="y")]
        self.FigGrid = [
            QtWidgets.QGridLayout(self.FigQGB[0]),
            QtWidgets.QGridLayout(self.FigQGB[1]),
        ]
        self.FigGrid[0].setObjectName("FigGrid_0")
        self.FigGrid[0].addWidget(self.pw[0])
        self.FigGrid[1].setObjectName("FigGrid_1")
        self.FigGrid[1].addWidget(self.pw[1])

        self.FuncQGB = QtWidgets.QGroupBox(self.centralwidget)
        self.FuncQGB.setObjectName("FuncQGB_0")
        self.FuncQGB.setGeometry(QtCore.QRect(x, y, funcW, funcH))

        self.synchLabel = QtWidgets.QLabel("输出方式")
        self.synchLabel.setObjectName("synchLabel")
        self.synchSelect = QtWidgets.QComboBox()
        self.synchSelect.setObjectName("synchSelect")
        self.synchSelect.addItems(("异步", "同步"))
        self.synchSelect.setCurrentIndex(0)

        self.channelLabel = [
            QtWidgets.QLabel("通道1"),
            QtWidgets.QLabel("通道2"),
        ]
        self.waveSelect = [
            QtWidgets.QComboBox(),
            QtWidgets.QComboBox(),
        ]
        self.channelLabel[0].setObjectName("channelLabel_0")
        self.waveSelect[0].setObjectName("waveSelect_0")
        self.waveSelect[0].addItems(
            ("关闭", "正弦波", "方波", "直流", "三角波", "锯齿波", "表达式", "文件")
        )
        self.waveSelect[0].setCurrentIndex(0)
        self.channelLabel[1].setObjectName("channelLabel_1")
        self.waveSelect[1].setObjectName("waveSelect_1")
        self.waveSelect[1].addItems(
            ("关闭", "正弦波", "方波", "直流", "三角波", "锯齿波", "表达式", "文件")
        )
        self.waveSelect[1].setCurrentIndex(0)

        self.freqLabel = [
            QtWidgets.QLabel("频率/Hz"),
            QtWidgets.QLabel("频率/Hz"),
        ]
        self.freqInput = [
            QtWidgets.QDoubleSpinBox(),
            QtWidgets.QDoubleSpinBox(),
        ]
        self.freqLabel[0].setObjectName("freqLabel_0")
        self.freqInput[0].setMinimum(0.01)
        self.freqInput[0].setMaximum(20000.0)
        self.freqInput[0].setObjectName("freqInput_0")
        self.freqInput[0].setValue(100)
        self.freqLabel[1].setObjectName("freqLabel_1")
        self.freqInput[1].setMinimum(0.01)
        self.freqInput[1].setMaximum(20000.0)
        self.freqInput[1].setObjectName("freqInput_1")
        self.freqInput[1].setValue(100)

        self.ampLabel = [
            QtWidgets.QLabel("幅度/V"),
            QtWidgets.QLabel("幅度/V"),
        ]
        self.ampInput = [
            QtWidgets.QDoubleSpinBox(),
            QtWidgets.QDoubleSpinBox(),
        ]
        self.ampLabel[0].setObjectName("ampLabel_0")
        self.ampInput[0].setSingleStep(0.1)
        self.ampInput[0].setObjectName("ampInput_0")
        self.ampInput[0].setValue(5)
        self.ampLabel[1].setObjectName("ampLabel_1")
        self.ampInput[1].setSingleStep(0.1)
        self.ampInput[1].setObjectName("ampInput_1")
        self.ampInput[1].setValue(5)

        self.offsetLabel = [
            QtWidgets.QLabel("偏置/V"),
            QtWidgets.QLabel("偏置/V"),
        ]
        self.offsetInput = [
            QtWidgets.QDoubleSpinBox(),
            QtWidgets.QDoubleSpinBox(),
        ]
        self.offsetLabel[0].setObjectName("offsetLabel_0")
        self.offsetInput[0].setSingleStep(0.1)
        self.offsetInput[0].setObjectName("offsetInput_0")
        self.offsetInput[0].setValue(0)
        self.offsetInput[0].setRange(-10, 10)
        self.offsetLabel[1].setObjectName("offsetLabel_1")
        self.offsetInput[1].setSingleStep(0.1)
        self.offsetInput[1].setObjectName("offsetInput_1")
        self.offsetInput[1].setValue(0)
        self.offsetInput[1].setRange(-10, 10)

        self.dutyLabel = [
            QtWidgets.QLabel("占空比/%"),
            QtWidgets.QLabel("占空比/%"),
        ]
        self.dutyInput = [
            QtWidgets.QDoubleSpinBox(),
            QtWidgets.QDoubleSpinBox(),
        ]
        self.dutyLabel[0].setObjectName("dutyLabel_0")
        self.dutyInput[0].setMaximum(100.0)
        self.dutyInput[0].setSingleStep(10.0)
        self.dutyInput[0].setObjectName("dutyInput_0")
        self.dutyInput[0].setValue(50)
        self.dutyLabel[1].setObjectName("dutyLabel_1")
        self.dutyInput[1].setMaximum(100.0)
        self.dutyInput[1].setSingleStep(10.0)
        self.dutyInput[1].setObjectName("dutyInput_1")
        self.dutyInput[1].setValue(50)

        self.phiLabel = [
            QtWidgets.QLabel("相位/°"),
            QtWidgets.QLabel("相位/°"),
        ]
        self.phiInput = [
            QtWidgets.QDoubleSpinBox(),
            QtWidgets.QDoubleSpinBox(),
        ]
        self.phiLabel[0].setObjectName("phiLabel_0")
        self.phiInput[0].setMaximum(360.0)
        self.phiInput[0].setSingleStep(10)
        self.phiInput[0].setObjectName("phiInput_0")
        self.phiInput[0].setValue(0)
        self.phiLabel[1].setObjectName("phiLabel_1")
        self.phiInput[1].setMaximum(360.0)
        self.phiInput[1].setSingleStep(10)
        self.phiInput[1].setObjectName("phiInput_1")
        self.phiInput[1].setValue(0)

        self.expLabel = [
            QtWidgets.QLabel("表达式"),
            QtWidgets.QLabel("表达式"),
        ]
        self.expInput = [
            QtWidgets.QLineEdit(),
            QtWidgets.QLineEdit(),
        ]
        self.expLabel[0].setObjectName("expLabel_0")
        self.expInput[0].setObjectName("expInput_0")
        self.expInput[0].setText("0,1;sin(2*pi*100*t)")
        self.expLabel[1].setObjectName("expLabel_1")
        self.expLabel[1].adjustSize()
        self.expInput[1].setObjectName("expInput_1")
        self.expInput[1].setText("0,1;sin(2*pi*100*t)")

        self.fileLabel = [
            QtWidgets.QLabel("文件名"),
            QtWidgets.QLabel("文件名"),
        ]
        self.fileInput = [
            QtWidgets.QLineEdit(),
            QtWidgets.QLineEdit(),
        ]
        self.fileLabel[0].setObjectName("fileLabel_0")
        self.fileInput[0].setObjectName("fileInput_0")
        self.fileLabel[1].setObjectName("fileLabel_1")
        self.fileInput[1].setObjectName("fileInput_1")

        self.FuncGrid = QtWidgets.QGridLayout(self.FuncQGB)
        self.FuncGrid.setObjectName("FuncGrid")
        self.FuncGrid.setHorizontalSpacing(50)
        self.FuncGrid.setHorizontalSpacing(50)

        self.FuncGrid.addWidget(self.synchLabel, 0, 0)
        self.FuncGrid.addWidget(self.synchSelect, 0, 1)
        self.FuncGrid.addWidget(self.channelLabel[0], 1, 0)
        self.FuncGrid.addWidget(self.waveSelect[0], 1, 1)
        self.FuncGrid.addWidget(self.channelLabel[1], 1, 2)
        self.FuncGrid.addWidget(self.waveSelect[1], 1, 3)
        self.FuncGrid.addWidget(self.freqLabel[0], 2, 0)
        self.FuncGrid.addWidget(self.freqInput[0], 2, 1)
        self.FuncGrid.addWidget(self.freqLabel[1], 2, 2)
        self.FuncGrid.addWidget(self.freqInput[1], 2, 3)
        self.FuncGrid.addWidget(self.ampLabel[0], 3, 0)
        self.FuncGrid.addWidget(self.ampInput[0], 3, 1)
        self.FuncGrid.addWidget(self.ampLabel[1], 3, 2)
        self.FuncGrid.addWidget(self.ampInput[1], 3, 3)
        self.FuncGrid.addWidget(self.offsetLabel[0], 4, 0)
        self.FuncGrid.addWidget(self.offsetInput[0], 4, 1)
        self.FuncGrid.addWidget(self.offsetLabel[1], 4, 2)
        self.FuncGrid.addWidget(self.offsetInput[1], 4, 3)
        self.FuncGrid.addWidget(self.dutyLabel[0], 5, 0)
        self.FuncGrid.addWidget(self.dutyInput[0], 5, 1)
        self.FuncGrid.addWidget(self.dutyLabel[1], 5, 2)
        self.FuncGrid.addWidget(self.dutyInput[1], 5, 3)
        self.FuncGrid.addWidget(self.phiLabel[0], 6, 0)
        self.FuncGrid.addWidget(self.phiInput[0], 6, 1)
        self.FuncGrid.addWidget(self.phiLabel[1], 6, 2)
        self.FuncGrid.addWidget(self.phiInput[1], 6, 3)
        self.FuncGrid.addWidget(self.expLabel[0], 7, 0)
        self.FuncGrid.addWidget(self.expInput[0], 7, 1)
        self.FuncGrid.addWidget(self.expLabel[1], 7, 2)
        self.FuncGrid.addWidget(self.expInput[1], 7, 3)
        self.FuncGrid.addWidget(self.fileLabel[0], 8, 0)
        self.FuncGrid.addWidget(self.fileInput[0], 8, 1)
        self.FuncGrid.addWidget(self.fileLabel[1], 8, 2)
        self.FuncGrid.addWidget(self.fileInput[1], 8, 3)

        self.setCentralWidget(self.centralwidget)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_SignalGenerator()
    ui.show()
    sys.exit(app.exec_())
