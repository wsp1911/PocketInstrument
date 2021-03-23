from PyQt5 import QtGui


def clicked(button):
    if button.text() == "Turn on":
        button.setText("Turn off")
        button.setFont(QtGui.QFont("宋体", 14))
        button.setStyleSheet("background-color: red;")
    else:
        button.setText("Turn on")
        button.setFont(QtGui.QFont("宋体", 14))
        button.setStyleSheet("background-color: green;")
