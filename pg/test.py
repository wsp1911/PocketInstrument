# -*- coding: utf-8 -*-
"""
Simple demonstration of TableWidget, which is an extension of QTableWidget
that automatically displays a variety of tabluar data formats.
"""
# import initExample  ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

app = QtGui.QApplication([])

w = pg.TableWidget()
w.show()
w.resize(500, 500)
w.setWindowTitle("pyqtgraph example: TableWidget")


data = np.array(["x", "0", "y", "0", "z", "0", "w", "0"])

w.setData(data)
# w.setEditable(True)
# w.background = "b"


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == "__main__":
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, "PYQT_VERSION"):
        QtGui.QApplication.instance().exec_()
