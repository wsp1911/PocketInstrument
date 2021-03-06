from PyQt5.QtWidgets import QDoubleSpinBox, QSlider, QMainWindow, QApplication
import numpy as np
import wave
from scipy import signal
from scipy.io import savemat, loadmat
import pandas as pd
import sys


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


class myPlotWidget(pg.PlotWidget):
    def setRange(
        self,
        rect=None,
        xRange=None,
        yRange=None,
        padding=None,
        update=True,
        disableAutoRange=True,
    ):
        """
        Set the visible range of the ViewBox.
        Must specify at least one of *rect*, *xRange*, or *yRange*.

        ================== =====================================================================
        **Arguments:**
        *rect*             (QRectF) The full range that should be visible in the view box.
        *xRange*           (min,max) The range that should be visible along the x-axis.
        *yRange*           (min,max) The range that should be visible along the y-axis.
        *padding*          (float) Expand the view by a fraction of the requested range.
                           By default, this value is set between 0.02 and 0.1 depending on
                           the size of the ViewBox.
        *update*           (bool) If True, update the range of the ViewBox immediately.
                           Otherwise, the update is deferred until before the next render.
        *disableAutoRange* (bool) If True, auto-ranging is diabled. Otherwise, it is left
                           unchanged.
        ================== =====================================================================

        """

        changes = {}  # axes
        setRequested = [False, False]

        if rect is not None:
            changes = {0: [rect.left(), rect.right()], 1: [rect.top(), rect.bottom()]}
            setRequested = [True, True]
        if xRange is not None:
            changes[0] = xRange
            setRequested[0] = True
        if yRange is not None:
            changes[1] = yRange
            setRequested[1] = True

        if len(changes) == 0:
            print(rect)
            raise Exception(
                "Must specify at least one of rect, xRange, or yRange. (gave rect=%s)"
                % str(type(rect))
            )

        # Update axes one at a time
        changed = [False, False]

        # Disable auto-range for each axis that was requested to be set
        if disableAutoRange:
            xOff = False if setRequested[0] else None
            yOff = False if setRequested[1] else None
            self.enableAutoRange(x=xOff, y=yOff)
            changed.append(True)

        limits = (self.state["limits"]["xLimits"], self.state["limits"]["yLimits"])
        minRng = [self.state["limits"]["xRange"][0], self.state["limits"]["yRange"][0]]
        maxRng = [self.state["limits"]["xRange"][1], self.state["limits"]["yRange"][1]]

        for ax, range in changes.items():
            mn = min(range)
            mx = max(range)

            # If we requested 0 range, try to preserve previous scale.
            # Otherwise just pick an arbitrary scale.
            if mn == mx:
                dy = self.state["viewRange"][ax][1] - self.state["viewRange"][ax][0]
                if dy == 0:
                    dy = 1
                mn -= dy * 0.5
                mx += dy * 0.5
                xpad = 0.0

            # Make sure no nan/inf get through
            if not all(np.isfinite([mn, mx])):
                raise Exception("Cannot set range [%s, %s]" % (str(mn), str(mx)))

            # Apply padding
            if padding is None:
                xpad = self.suggestPadding(ax)
            else:
                xpad = padding
            p = (mx - mn) * xpad
            mn -= p
            mx += p

            # max range cannot be larger than bounds, if they are given
            if limits[ax][0] is not None and limits[ax][1] is not None:
                if maxRng[ax] is not None:
                    maxRng[ax] = min(maxRng[ax], limits[ax][1] - limits[ax][0])
                else:
                    maxRng[ax] = limits[ax][1] - limits[ax][0]

            # If we have limits, we will have at least a max range as well
            if maxRng[ax] is not None or minRng[ax] is not None:
                diff = mx - mn
                if maxRng[ax] is not None and diff > maxRng[ax]:
                    delta = maxRng[ax] - diff
                elif minRng[ax] is not None and diff < minRng[ax]:
                    delta = minRng[ax] - diff
                else:
                    delta = 0

                mn -= delta / 2.0
                mx += delta / 2.0

            # Make sure our requested area is within limits, if any
            if limits[ax][0] is not None or limits[ax][1] is not None:
                lmn, lmx = limits[ax]
                if lmn is not None and mn < lmn:
                    delta = (
                        lmn - mn
                    )  # Shift the requested view to match our lower limit
                    mn = lmn
                    mx += delta
                elif lmx is not None and mx > lmx:
                    delta = lmx - mx
                    mx = lmx
                    mn += delta

            # Set target range
            if self.state["targetRange"][ax] != [mn, mx]:
                self.state["targetRange"][ax] = [mn, mx]
                changed[ax] = True

        # Update viewRange to match targetRange as closely as possible while
        # accounting for aspect ratio constraint
        lockX, lockY = setRequested
        if lockX and lockY:
            lockX = False
            lockY = False
        self.updateViewRange(lockX, lockY)

        # If nothing has changed, we are done.
        if any(changed):
            # Update target rect for debugging
            if self.target.isVisible():
                self.target.setRect(
                    self.mapRectFromItem(self.childGroup, self.targetRect())
                )

            # If ortho axes have auto-visible-only, update them now
            # Note that aspect ratio constraints and auto-visible probably do not work together..
            if (
                changed[0]
                and self.state["autoVisibleOnly"][1]
                and (self.state["autoRange"][0] is not False)
            ):
                self._autoRangeNeedsUpdate = True
            elif (
                changed[1]
                and self.state["autoVisibleOnly"][0]
                and (self.state["autoRange"][1] is not False)
            ):
                self._autoRangeNeedsUpdate = True

            self.sigStateChanged.emit(self)


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
