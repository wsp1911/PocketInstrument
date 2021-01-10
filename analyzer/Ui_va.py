# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\Project\Python\PocketInstrument\analyzer\va.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class logSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, parent=None):
        super(logSpinBox, self).__init__(parent)
        super(logSpinBox, self).setMinimum(0.01)
        super(logSpinBox, self).setMaximum(100)
        super(logSpinBox, self).setSingleStep(2)
        super(logSpinBox, self).setValue(1)
        self.refreshVals()

    def stepBy(self, steps):
        if 0 <= self.__idx + steps < len(self.__vals):
            self.__idx += steps
            super(logSpinBox, self).setValue(self.__vals[self.__idx])

    def setSingleStep(self, step):
        if step > 1:
            super(logSpinBox, self).setSingleStep(step)
            self.refreshVals()
        elif 0 < step < 1:
            super(logSpinBox, self).setSingleStep(1 / step)
            self.refreshVals()

    def setParameters(self, mi, ma, step, decimal):
        if 0 < mi < 1:
            super(logSpinBox, self).setMinimum(mi)
        if ma > 1:
            super(logSpinBox, self).setMaximum(ma)
        if step > 1:
            super(logSpinBox, self).setSingleStep(step)
        elif 0 < step < 1:
            super(logSpinBox, self).setSingleStep(1 / step)
        super(logSpinBox, self).setDecimals(decimal)
        self.refreshVals()

    def refreshVals(self):
        self.__vals = [1]
        self.__idx = 0
        super(logSpinBox, self).setValue(1)
        mi = self.minimum() * self.singleStep()
        ma = self.maximum() / self.singleStep()
        while self.__vals[0] > mi:
            self.__vals.insert(
                0, round(self.__vals[0] / self.singleStep(), self.decimals())
            )
            self.__idx += 1
        self.__vals.insert(0, round(self.minimum(), self.decimals()))
        self.__idx += 1
        while self.__vals[-1] < ma:
            self.__vals.append(
                round(self.__vals[-1] * self.singleStep(), self.decimals())
            )
        self.__vals.append(round(self.maximum(), self.decimals()))

    def setMinimum(self, mi):
        if 0 < mi < 1:
            super(logSpinBox, self).setMinimum(mi)
            self.refreshVals()

    def setMaximum(self, ma):
        if ma > 1:
            super(logSpinBox, self).setMaximum(ma)
            self.refreshVals()

    def setValue(self, val):
        if self.minimum() <= val <= self.maximum():
            for i in range(1, len(self.__vals)):
                if self.__vals[i - 1] <= val <= self.__vals[i]:
                    if val - self.__vals[i - 1] < self.__vals[i] - val:
                        super(logSpinBox, self).setValue(self.__vals[i - 1])
                        self.__idx = i - 1
                    else:
                        super(logSpinBox, self).setValue(self.__vals[i])
                        self.__idx = i
                    return


class doubleSlider(QtWidgets.QSlider):
    def __init__(self, parent=None):
        super(doubleSlider, self).__init__(parent)
        super(doubleSlider, self).setMinimum(0)
        super(doubleSlider, self).setMaximum(100)

        self.__mi, self.__ma, self.__step = 0, 1, 0.01

    def setParameters(self, mi, ma, num):
        self.__mi, self.__ma = mi, ma
        super(doubleSlider, self).setMaximum(num)
        self.__step = (ma - mi) / num

    def value(self):
        return self.__mi + super(doubleSlider, self).value() * self.__step

    def setValue(self, val):
        if self.__mi <= val <= self.__ma:
            super(doubleSlider, self).setValue(int((val - self.__mi) / self.__step))

    def maximum(self):
        return self.__ma

    def setMaximum(self, ma):
        if ma >= self.__mi:
            self.__ma = ma
            self.__step = (self.__ma - self.__mi) / (
                super(doubleSlider, self).maximum()
            )

    def minimum(self):
        return self.__mi

    def setMinimum(self, mi):
        if mi <= self.__ma:
            self.__mi = mi
            self.__step = (self.__ma - self.__mi) / (
                super(doubleSlider, self).maximum()
            )

    def setRange(self, mi, ma):
        if ma >= mi:
            self.__ma, self.__mi = ma, mi
            self.__step = (self.__ma - self.__mi) / (
                super(doubleSlider, self).maximum()
            )


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.desktop = QtWidgets.QApplication.desktop()

        # 获取显示器分辨率大小
        self.screenRect = self.desktop.screenGeometry()
        # self.height = self.screenRect.height()
        # self.width = self.screenRect.width()
        # WIDTH, HEIGHT = 1800, 1000
        WIDTH = int(0.9 * self.screenRect.width())
        HEIGHT = int(0.9 * self.screenRect.height())

        marginL, marginU, windY = 0, 0, 0

        winW, winH = 2 * WIDTH // 3, HEIGHT - 2 * marginU - windY
        tWinH = HEIGHT
        # tWinH = HEIGHT * 2 // 3
        # fWinH = winH - tWinH

        sliderX, sliderY = winW + 2 * marginL, 0
        sliderW, sliderH = 10, int(0.7 * HEIGHT)
        sx = [i * sliderW + sliderX for i in range(4)]

        itemW, itemH = 100, 40
        btnW, btnH = itemW, 40
        labelW, labelH = itemW, itemH
        inputW, inputH = itemW, itemH
        multiW, multiH = itemW, itemH
        funcW, funcH = WIDTH - winW - 2 * marginL - 5 * sliderW, HEIGHT
        funcX, funcY = winW + 2 * marginL + 4 * sliderW, 0
        itemW = max([btnW, labelW, inputW])
        itemNX, itemNY = 5, 20
        itemdX = (funcW - itemNX * itemW) // (itemNX - 1)
        itemdY = (funcH - itemNY * itemH) // (itemNY - 1)
        x = [funcX + i * (itemW + itemdX) for i in range(itemNX)]
        y = [funcY + i * (itemH + itemdY) for i in range(itemNY)]

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(WIDTH, HEIGHT)
        MainWindow.setFont(QtGui.QFont("宋体", 14))
        MainWindow.setWindowTitle("示波器")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.TimeQGB = QtWidgets.QGroupBox(self.centralwidget)
        self.TimeQGB.setGeometry(QtCore.QRect(marginL, marginU, winW, tWinH))
        self.TimeQGB.setObjectName("TimeQGB")

        self.CursorX, self.CursorY = [], []
        self.CursorX.append(doubleSlider(self.centralwidget))
        self.CursorX[0].setGeometry(QtCore.QRect(sx[0], sliderY, sliderW, sliderH))
        self.CursorX[0].setOrientation(QtCore.Qt.Vertical)
        self.CursorX[0].setObjectName("CursorX1")

        self.CursorX.append(doubleSlider(self.centralwidget))
        self.CursorX[1].setGeometry(QtCore.QRect(sx[1], sliderY, sliderW, sliderH))
        self.CursorX[1].setOrientation(QtCore.Qt.Vertical)
        self.CursorX[1].setObjectName("CursorX2")

        self.CursorY.append(doubleSlider(self.centralwidget))
        self.CursorY[0].setGeometry(QtCore.QRect(sx[2], sliderY, sliderW, sliderH))
        self.CursorY[0].setOrientation(QtCore.Qt.Vertical)
        self.CursorY[0].setObjectName("CursorY1")
        self.CursorY[0].setParameters(-10, 10, 1000)

        self.CursorY.append(doubleSlider(self.centralwidget))
        self.CursorY[1].setGeometry(QtCore.QRect(sx[3], sliderY, sliderW, sliderH))
        self.CursorY[1].setOrientation(QtCore.Qt.Vertical)
        self.CursorY[1].setObjectName("CursorY2")
        self.CursorY[1].setParameters(-10, 10, 1000)

        self.Trigger = doubleSlider(self.centralwidget)
        self.Trigger.setGeometry(
            QtCore.QRect(WIDTH - sliderW, sliderY, sliderW, sliderH)
        )
        self.Trigger.setOrientation(QtCore.Qt.Vertical)
        self.Trigger.setObjectName("Trigger")
        self.Trigger.setParameters(-10, 10, 1000)
        self.Trigger.setValue(0)

        # self.FreqQGB = QtWidgets.QGroupBox(self.centralwidget)
        # self.FreqQGB.setGeometry(
        #     QtCore.QRect(marginL, marginU + tWinH + windY, winW, fWinH)
        # )
        # self.FreqQGB.setObjectName("FreqQGB")

        i, j = 0, 0
        self.HorizontalLabel = QtWidgets.QLabel(self.centralwidget)
        self.HorizontalLabel.setGeometry(QtCore.QRect(x[i], y[j], labelW, labelH))
        self.HorizontalLabel.setObjectName("HorizontalLabel")
        self.HorizontalLabel.setText("水平")

        self.tZoomLabel = QtWidgets.QLabel(self.centralwidget)
        self.tZoomLabel.setGeometry(QtCore.QRect(x[i], y[j + 1], labelW, labelH))
        self.tZoomLabel.setObjectName("tZoomLabel")
        self.tZoomLabel.setText("Zoom")
        self.tZoomInput = logSpinBox(self.centralwidget)
        self.tZoomInput.setGeometry(QtCore.QRect(x[i + 1], y[j + 1], inputW, inputH))
        self.tZoomInput.setObjectName("tZoomInput")
        self.tZoomInput.setParameters(mi=0.125, ma=10, step=0.5, decimal=3)

        self.RunButton = QtWidgets.QPushButton(self.centralwidget)
        self.RunButton.setGeometry(QtCore.QRect(x[-1], y[0], btnW, btnH))
        self.RunButton.setObjectName("RunButton")

        i, j = 0, 2
        self.MeasureLabel = QtWidgets.QLabel(self.centralwidget)
        self.MeasureLabel.setGeometry(QtCore.QRect(x[i], y[j], labelW, labelH))
        self.MeasureLabel.setObjectName("MeasureLabel")
        self.MeasureLabel.setText("测量")

        self.MeasureSourceLabel = QtWidgets.QLabel(self.centralwidget)
        self.MeasureSourceLabel.setGeometry(
            QtCore.QRect(x[i], y[j + 1], labelW, labelH)
        )
        self.MeasureSourceLabel.setObjectName("MeasureSourceLabel")
        self.MeasureSourceLabel.setText("源")

        self.MeasChanMultiple = QtWidgets.QComboBox(self.centralwidget)
        self.MeasChanMultiple.setGeometry(
            QtCore.QRect(x[i + 1], y[j + 1], multiW, multiH)
        )
        self.MeasChanMultiple.setObjectName("MeasChanMultiple")
        self.MeasChanMultiple.addItems(("1", "2"))

        self.CursorLabel = QtWidgets.QLabel(self.centralwidget)
        self.CursorLabel.setGeometry(QtCore.QRect(x[i], y[j + 2], labelW, labelH))
        self.CursorLabel.setObjectName("CursorLabel")
        self.CursorLabel.setText("Cursor")
        self.CursorButton = QtWidgets.QPushButton(self.centralwidget)
        self.CursorButton.setGeometry(QtCore.QRect(x[i + 1], y[j + 2], btnW, btnH))
        self.CursorButton.setObjectName("CursorButton")

        i, j = 3, 2
        self.TriggerLabel = QtWidgets.QLabel(self.centralwidget)
        self.TriggerLabel.setGeometry(QtCore.QRect(x[i], y[j], labelW, labelH))
        self.TriggerLabel.setObjectName("TriggerLabel")
        self.TriggerLabel.setText("触发")
        self.TriggerSourceLabel = QtWidgets.QLabel(self.centralwidget)
        self.TriggerSourceLabel.setGeometry(
            QtCore.QRect(x[i], y[j + 1], labelW, labelH)
        )
        self.TriggerSourceLabel.setObjectName("TriggerSourceLabel")
        self.TriggerSourceLabel.setText("源")
        self.TriggerChanMultiple = QtWidgets.QComboBox(self.centralwidget)
        self.TriggerChanMultiple.setGeometry(
            QtCore.QRect(x[i + 1], y[j + 1], multiW, multiH)
        )
        self.TriggerChanMultiple.setObjectName("TriggerChanMultiple")
        self.TriggerChanMultiple.addItems(("1", "2"))
        self.TriggerSlopeLabel = QtWidgets.QLabel(self.centralwidget)
        self.TriggerSlopeLabel.setGeometry(QtCore.QRect(x[i], y[j + 2], labelW, labelH))
        self.TriggerSlopeLabel.setObjectName("TriggerSlopeLabel")
        self.TriggerSlopeLabel.setText("Slope")
        self.TriggerSlopeMultiple = QtWidgets.QComboBox(self.centralwidget)
        self.TriggerSlopeMultiple.setGeometry(
            QtCore.QRect(x[i + 1], y[j + 2], multiW, multiH)
        )
        self.TriggerSlopeMultiple.setObjectName("TriggerSlopeMultiple")
        self.TriggerSlopeMultiple.addItems(("pos", "neg"))

        (
            self.ChannelLabel,
            self.ZoomLabel,
            self.ZoomInput,
            self.OffsetLabel,
            self.OffsetInput,
        ) = ([], [], [], [], [])

        i, j = 0, -5
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

        i, j = 3, -5
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
        # self.OffsetInput[1].setValue(1)
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
        self.CursorButton.setText(_translate("MainWindow", "Off"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
