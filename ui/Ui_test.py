# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\Project\Python\PocketInstrument\ui\test.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 492)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TurnOn = QtWidgets.QPushButton(self.centralwidget)
        self.TurnOn.setGeometry(QtCore.QRect(60, 320, 75, 23))
        self.TurnOn.setObjectName("TurnOn")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 110, 45, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 45, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 190, 45, 21))
        self.label_3.setObjectName("label_3")
        self.TurnOff = QtWidgets.QPushButton(self.centralwidget)
        self.TurnOff.setGeometry(QtCore.QRect(60, 360, 75, 23))
        self.TurnOff.setObjectName("TurnOff")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(70, 240, 54, 12))
        self.label_4.setObjectName("label_4")
        self.freqInput = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.freqInput.setGeometry(QtCore.QRect(130, 110, 62, 22))
        self.freqInput.setMaximum(20000.0)
        self.freqInput.setObjectName("freqInput")
        self.ampInput = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ampInput.setGeometry(QtCore.QRect(130, 150, 62, 22))
        self.ampInput.setSingleStep(0.1)
        self.ampInput.setObjectName("ampInput")
        self.phiInput = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.phiInput.setGeometry(QtCore.QRect(130, 190, 62, 22))
        self.phiInput.setMaximum(360.0)
        self.phiInput.setObjectName("phiInput")
        self.offsetInput = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.offsetInput.setGeometry(QtCore.QRect(130, 240, 62, 22))
        self.offsetInput.setSingleStep(0.1)
        self.offsetInput.setObjectName("offsetInput")
        self.freqMultiple = QtWidgets.QComboBox(self.centralwidget)
        self.freqMultiple.setGeometry(QtCore.QRect(200, 110, 71, 22))
        self.freqMultiple.setObjectName("freqMultiple")
        self.waveSelect = QtWidgets.QComboBox(self.centralwidget)
        self.waveSelect.setGeometry(QtCore.QRect(130, 60, 71, 22))
        self.waveSelect.setObjectName("waveSelect")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(70, 70, 54, 12))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(70, 280, 54, 12))
        self.label_6.setObjectName("label_6")
        self.dutyInput = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.dutyInput.setGeometry(QtCore.QRect(130, 280, 62, 22))
        self.dutyInput.setMaximum(100.0)
        self.dutyInput.setSingleStep(10.0)
        self.dutyInput.setObjectName("dutyInput")
        self.ampMultiple = QtWidgets.QComboBox(self.centralwidget)
        self.ampMultiple.setGeometry(QtCore.QRect(200, 150, 71, 22))
        self.ampMultiple.setObjectName("ampMultiple")
        self.phiMultiple = QtWidgets.QComboBox(self.centralwidget)
        self.phiMultiple.setGeometry(QtCore.QRect(200, 190, 71, 22))
        self.phiMultiple.setObjectName("phiMultiple")
        self.offsetMultiple = QtWidgets.QComboBox(self.centralwidget)
        self.offsetMultiple.setGeometry(QtCore.QRect(200, 240, 71, 22))
        self.offsetMultiple.setObjectName("offsetMultiple")
        self.dutyMultiple = QtWidgets.QComboBox(self.centralwidget)
        self.dutyMultiple.setGeometry(QtCore.QRect(200, 280, 71, 22))
        self.dutyMultiple.setObjectName("dutyMultiple")
        self.ampInput_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ampInput_2.setGeometry(QtCore.QRect(360, 150, 62, 22))
        self.ampInput_2.setSingleStep(0.1)
        self.ampInput_2.setObjectName("ampInput_2")
        self.dutyMultiple_2 = QtWidgets.QComboBox(self.centralwidget)
        self.dutyMultiple_2.setGeometry(QtCore.QRect(430, 280, 71, 22))
        self.dutyMultiple_2.setObjectName("dutyMultiple_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(300, 70, 54, 12))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(300, 190, 45, 21))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(300, 110, 45, 21))
        self.label_9.setObjectName("label_9")
        self.phiInput_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.phiInput_2.setGeometry(QtCore.QRect(360, 190, 62, 22))
        self.phiInput_2.setMaximum(360.0)
        self.phiInput_2.setObjectName("phiInput_2")
        self.freqInput_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.freqInput_2.setGeometry(QtCore.QRect(360, 110, 62, 22))
        self.freqInput_2.setMaximum(20000.0)
        self.freqInput_2.setObjectName("freqInput_2")
        self.offsetMultiple_2 = QtWidgets.QComboBox(self.centralwidget)
        self.offsetMultiple_2.setGeometry(QtCore.QRect(430, 240, 71, 22))
        self.offsetMultiple_2.setObjectName("offsetMultiple_2")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(300, 150, 45, 21))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(300, 240, 54, 12))
        self.label_11.setObjectName("label_11")
        self.ampMultiple_2 = QtWidgets.QComboBox(self.centralwidget)
        self.ampMultiple_2.setGeometry(QtCore.QRect(430, 150, 71, 22))
        self.ampMultiple_2.setObjectName("ampMultiple_2")
        self.TurnOff_2 = QtWidgets.QPushButton(self.centralwidget)
        self.TurnOff_2.setGeometry(QtCore.QRect(290, 360, 75, 23))
        self.TurnOff_2.setObjectName("TurnOff_2")
        self.freqMultiple_2 = QtWidgets.QComboBox(self.centralwidget)
        self.freqMultiple_2.setGeometry(QtCore.QRect(430, 110, 71, 22))
        self.freqMultiple_2.setObjectName("freqMultiple_2")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(300, 280, 54, 12))
        self.label_12.setObjectName("label_12")
        self.dutyInput_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.dutyInput_2.setGeometry(QtCore.QRect(360, 280, 62, 22))
        self.dutyInput_2.setMaximum(100.0)
        self.dutyInput_2.setSingleStep(10.0)
        self.dutyInput_2.setObjectName("dutyInput_2")
        self.offsetInput_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.offsetInput_2.setGeometry(QtCore.QRect(360, 240, 62, 22))
        self.offsetInput_2.setSingleStep(0.1)
        self.offsetInput_2.setObjectName("offsetInput_2")
        self.waveSelect_2 = QtWidgets.QComboBox(self.centralwidget)
        self.waveSelect_2.setGeometry(QtCore.QRect(360, 60, 71, 22))
        self.waveSelect_2.setObjectName("waveSelect_2")
        self.TurnOn_2 = QtWidgets.QPushButton(self.centralwidget)
        self.TurnOn_2.setGeometry(QtCore.QRect(290, 320, 75, 23))
        self.TurnOn_2.setObjectName("TurnOn_2")
        self.phiMultiple_2 = QtWidgets.QComboBox(self.centralwidget)
        self.phiMultiple_2.setGeometry(QtCore.QRect(430, 190, 71, 22))
        self.phiMultiple_2.setObjectName("phiMultiple_2")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(70, 20, 54, 12))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(300, 20, 54, 12))
        self.label_14.setObjectName("label_14")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TurnOn.setText(_translate("MainWindow", "Turn on"))
        self.label.setText(_translate("MainWindow", "频率"))
        self.label_2.setText(_translate("MainWindow", "幅度"))
        self.label_3.setText(_translate("MainWindow", "相位"))
        self.TurnOff.setText(_translate("MainWindow", "Turn off"))
        self.label_4.setText(_translate("MainWindow", "偏置"))
        self.label_5.setText(_translate("MainWindow", "波形"))
        self.label_6.setText(_translate("MainWindow", "占空比"))
        self.label_7.setText(_translate("MainWindow", "波形"))
        self.label_8.setText(_translate("MainWindow", "相位"))
        self.label_9.setText(_translate("MainWindow", "频率"))
        self.label_10.setText(_translate("MainWindow", "幅度"))
        self.label_11.setText(_translate("MainWindow", "偏置"))
        self.TurnOff_2.setText(_translate("MainWindow", "Turn off"))
        self.label_12.setText(_translate("MainWindow", "占空比"))
        self.TurnOn_2.setText(_translate("MainWindow", "Turn on"))
        self.label_13.setText(_translate("MainWindow", "通道1"))
        self.label_14.setText(_translate("MainWindow", "通道2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())