import sounddevice as sd
import numpy as np


def get_output_device_id_by_name(channel_name):
    """
    功能: 根据声卡声道名字, 获取 输出 声道 id
    :return: 返回输出声道id
    """
    devices_list = sd.query_devices()
    for index, device_msg_dict in enumerate(devices_list):
        if (
            channel_name == device_msg_dict["name"]
            and device_msg_dict["max_output_channels"] > 0
        ):
            return index
    else:
        print("找不到该设备！")
        return None


def genSineWave(sample_rate, freq, amp, phi, offset):
    x = np.arange(0, 10 / freq, 1 / sample_rate)
    y = offset + amp * np.sin(2 * np.pi * freq * x + phi / 180 * np.pi)
    return y


def genSquareWave(sample_rate, freq, amp, dutyRatio, offset):
    N = round(sample_rate / freq)
    x = np.arange(N)
    y = offset + (amp * (x < dutyRatio * N) - amp / 2)
    y = np.tile(y, 10).astype(np.float32)
    return y


def genSawtoothWave(sample_rate, freq, amp, offset):
    N = round(sample_rate / freq)
    y = offset + (np.linspace(0, amp, N) - amp / 2)
    y = np.tile(y, 10)
    return y


def genTriangleWave(sample_rate, freq, amp, width, offset):
    N = round(sample_rate / freq)
    N1 = round(N * width)
    y = (
        offset
        + np.r_[
            np.linspace(0, amp, N1), np.linspace(0, amp, N - N1, endpoint=False)[::-1]
        ]
    ) - amp / 2
    return np.r_[y[0], np.tile(y[1:], 10)]


def genDC(amp):
    return amp * np.ones(100)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    sample_rate = 44100
    freq = 1000
    amp = 1
    offset = 0
    phi = 0
    dutyRatio = 0.5
    y1 = genSineWave(sample_rate, freq, amp, phi, offset)
    y2 = genSquareWave(sample_rate, freq, amp, dutyRatio, offset)
    y3 = genSawtoothWave(sample_rate, freq, amp, offset)
    y4 = genTriangleWave(sample_rate, freq, amp, dutyRatio, offset)
    y5 = genDC(amp)
    M, N = 5, 1
    plt.subplot(M, N, 1)
    plt.plot(y1)
    plt.subplot(M, N, 2)
    plt.plot(y2)
    plt.subplot(M, N, 3)
    plt.plot(y3)
    plt.subplot(M, N, 4)
    plt.plot(y4)
    plt.subplot(M, N, 5)
    plt.plot(y5)
    plt.show()
