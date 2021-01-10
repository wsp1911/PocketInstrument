# -*- coding: utf-8 -*-
# Added by the Blog author VERtiCaL on 2020/07/12 at SSRF
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1613, 1308)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Plot_static = QtWidgets.QGroupBox(self.centralwidget)
        self.Plot_static.setGeometry(QtCore.QRect(260, 30, 861, 391))
        self.Plot_static.setObjectName("Plot_static")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(300, 830, 701, 91))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(28)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Static_plot = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Static_plot.sizePolicy().hasHeightForWidth())
        self.Static_plot.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.Static_plot.setFont(font)
        self.Static_plot.setObjectName("Static_plot")
        self.horizontalLayout.addWidget(self.Static_plot)
        self.dynamic_plot = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dynamic_plot.sizePolicy().hasHeightForWidth())
        self.dynamic_plot.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.dynamic_plot.setFont(font)
        self.dynamic_plot.setObjectName("dynamic_plot")
        self.horizontalLayout.addWidget(self.dynamic_plot)
        self.End_plot = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.End_plot.sizePolicy().hasHeightForWidth())
        self.End_plot.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(18)
        self.End_plot.setFont(font)
        self.End_plot.setObjectName("End_plot")
        self.horizontalLayout.addWidget(self.End_plot)
        self.Erase_plot = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Erase_plot.sizePolicy().hasHeightForWidth())
        self.Erase_plot.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(18)
        self.Erase_plot.setFont(font)
        self.Erase_plot.setObjectName("Erase_plot")
        self.horizontalLayout.addWidget(self.Erase_plot)
        self.Plot_dynamic = QtWidgets.QGroupBox(self.centralwidget)
        self.Plot_dynamic.setGeometry(QtCore.QRect(260, 430, 861, 391))
        self.Plot_dynamic.setObjectName("Plot_dynamic")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1613, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Plot_static.setTitle(_translate("MainWindow", "StaticPlot"))
        self.Static_plot.setText(_translate("MainWindow", "静态作图"))
        self.dynamic_plot.setText(_translate("MainWindow", "动态作图"))
        self.End_plot.setText(_translate("MainWindow", "停止作图"))
        self.Erase_plot.setText(_translate("MainWindow", "清除数据"))
        self.Plot_dynamic.setTitle(_translate("MainWindow", "DynamicPlot"))
