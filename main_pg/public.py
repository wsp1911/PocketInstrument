from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QSlider,
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QLabel,
)
from PyQt5.QtCore import Qt
import numpy as np
import wave
from scipy import signal
from scipy.io import savemat, loadmat
import pandas as pd
import sys


class DataGrid(QVBoxLayout):
    def __init__(self, parent=None, data_list={}):
        super(DataGrid, self).__init__(parent)
        self.data_dict = {}
        self.labels = []
        self.data = []
        for i in range(len(data_list[0])):
            self.labels.append(QLabel(data_list[0][i]))
            self.addWidget(self.labels[-1])
            self.data.append(QLabel(str(data_list[1][i]), alignment=Qt.AlignRight))
            self.addWidget(self.data[-1])
            self.data_dict[data_list[0][i]] = i

    def setData(self, key, s):
        self.data[self.data_dict[key]].setText(s)


class logSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super(logSpinBox, self).__init__(parent)
        self.__vals = []

    def stepBy(self, steps):
        if self.__vals:
            self.setValue(self.value())  # 用户输入后，更新idx
            if self.value() not in self.__vals and steps < 0:
                steps += 1
            if 0 <= self.__idx + steps < len(self.__vals):
                self.__idx += steps
                super(logSpinBox, self).setValue(self.__vals[self.__idx])
        else:
            super(logSpinBox, self).stepBy(steps)

    def setSingleStep(self, step):
        if step > 1:
            super(logSpinBox, self).setSingleStep(step)
            self.refreshVals()

    def setCenterValue(self, val):
        if self.minimum() <= val <= self.maximum():
            self.__center_val = val
            self.refreshVals()

    def setParameters(self, mi, ma, val, step, decimal):
        mi = round(mi, decimal)
        ma = round(ma, decimal)
        if 0 < mi <= val <= ma:
            super(logSpinBox, self).setMinimum(mi)
            super(logSpinBox, self).setMaximum(ma)
            self.__center_val = val
            if step > 1:
                super(logSpinBox, self).setSingleStep(step)
            self.setDecimals(decimal)
            self.refreshVals()
            super(logSpinBox, self).setValue(val)

    def refreshVals(self):
        self.__vals = [self.__center_val]
        self.__idx = 0
        step = self.singleStep()
        decimal = self.decimals()
        mi, ma = self.minimum() * step, self.maximum() / step

        tmp = self.__vals[0]
        while tmp > mi:
            self.__vals.insert(0, round(tmp / step, decimal))
            self.__idx += 1
            tmp /= step
        self.__vals.insert(0, self.minimum())
        self.__idx += 1

        tmp = self.__vals[-1]
        while tmp < ma:
            self.__vals.append(round(tmp * step, decimal))
            tmp *= step
        self.__vals.append(self.maximum())

    def setMinimum(self, mi):
        if 0 < mi <= self.__center_val <= self.maximum():
            super(logSpinBox, self).setMinimum(mi)
            self.refreshVals()

    def setMaximum(self, ma):
        if ma >= self.__center_val >= self.minimum():
            super(logSpinBox, self).setMaximum(ma)
            self.refreshVals()

    def setValue(self, val):
        if self.minimum() <= val <= self.maximum():
            super(logSpinBox, self).setValue(val)
            if val == self.maximum():
                self.__idx = len(self.__vals) - 1
            else:
                for i in range(len(self.__vals) - 1):
                    if self.__vals[i] <= val < self.__vals[i + 1]:
                        self.__idx = i
                        break

    def value(self):
        val = super(logSpinBox, self).value()
        if self.decimals() == 0:
            return int(val)
        return val


class doubleSlider(QSlider):
    def __init__(self, parent=None, num=10000):
        super(doubleSlider, self).__init__(parent)
        self.setParameters(0, 1, num)

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


def save_data(filename, data, out_format, channels=0, sampwidth=0, rate=0):
    if out_format == ".npy":
        np.save(filename + ".npy", data)
    elif out_format == ".mat":
        savemat(
            filename + ".mat",
            {"data": data},
        )
    elif out_format == ".txt":
        np.savetxt(filename + ".txt", data, "%5.5f")
    elif out_format == ".xlsx":
        data_df = pd.DataFrame(data)
        writer = pd.ExcelWriter(filename + ".xlsx")
        data_df.to_excel(writer, "page_1", float_format="%5.5f")
        writer.save()
    elif out_format == ".wav":
        wf = wave.open(filename + ".wav", "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(rate)
        wf.writeframes(data)
        wf.close()


def load_data(filename, fs=0):
    """
    not finished yet
    """
    try:
        # if filename[1] != ":":
        #     filename = sys.path[0] + "\\" + filename
        if filename[-4:].lower() == ".wav":
            f = wave.open(filename, "rb")
            params = f.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            strData = f.readframes(nframes)
            waveData = np.frombuffer(strData, dtype=np.int16)[::nchannels]
            waveData = waveData / 32768
            if framerate != fs:
                waveData = signal.resample_poly(waveData, fs, framerate)
            return waveData
        else:
            if filename[-4:].lower() == ".mat":
                data = loadmat(filename)
                data = data["data"].flatten()
            elif filename[-4:].lower() == ".npy":
                data = np.load(filename)
            elif filename[-4:].lower() == ".txt":
                data = np.loadtxt(filename)
            elif filename[-5:].lower() == ".xlsx":
                data_df = pd.read_excel(filename)
                data = data_df.values[:, 1:]
            return data
    except Exception:
        return False


if __name__ == "__main__":

    def func(a):
        print(a)

    app = QApplication(sys.argv)
    ui = QMainWindow()
    ui.resize(640, 480)
    test = logSpinBox(ui)
    test.setParameters(0.1, 10, 5, 2, 3)
    test.valueChanged.connect(func)

    ui.show()
    sys.exit(app.exec_())
