from PyQt5 import QtWidgets


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