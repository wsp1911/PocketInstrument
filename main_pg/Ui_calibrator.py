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


class Ui_Calibrator(QWidget):
    def __init__(self, parent=None):
        super(Ui_Calibrator, self).__init__(parent)
        WIDTH, HEIGHT = 400, 300

        self.font_size = 9
        self.Font = QFont("等线", self.font_size)
        self.setObjectName("calibrate")
        self.resize(WIDTH, HEIGHT)
        self.setFont(self.Font)
        self.setWindowTitle("校准")

        self.QGB = QGroupBox(self)
        self.QGB.setObjectName("QGB")
        self.QGB.setGeometry(QRect(0, 0, WIDTH, HEIGHT))

        self.calButton = QPushButton()
        self.calButton.setObjectName("calButton")
        self.calButton.setText("快速校准")

        self.Grid = QGridLayout(self.QGB)
        self.Grid.setObjectName("Grid")
        self.Grid.addWidget(self.calButton)

        QtCore.QMetaObject.connectSlotsByName(self)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = Ui_Calibrator()
    ui.show()
    sys.exit(app.exec_())
