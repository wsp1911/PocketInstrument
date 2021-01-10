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


def genSquareWave(sample_rate, freq, amp, dutyRatio, offset, t):
    N = round(sample_rate / freq)
    x = np.arange(N)
    y = offset + amp * (x < dutyRatio * N)
    y = np.tile(y, int(t * freq)).astype(np.float32)
    return y


def genSawtoothWave(sample_rate, freq, amp, offset, t):
    N = round(sample_rate / freq)
    N2 = 2
    y = np.r_[
        offset + np.linspace(0, amp, N - N2),
        np.linspace(amp + offset - amp / N2, offset, N2, endpoint=False),
    ]
    y = np.tile(y, int(t * freq))
    return y


def genTriangleWave(sample_rate, freq, amp, width, offset, t):
    N = round(sample_rate / freq)
    N1 = round(N * width)
    y = (
        offset
        + np.r_[
            np.linspace(0, amp, N1), np.linspace(0, amp, N - N1, endpoint=False)[::-1]
        ]
    )
    return np.r_[y[0], np.tile(y[1:], int(t * freq))]


output_id = get_output_device_id_by_name("扬声器 (EE Pocket Instrument)")
sample_rate = 44100
freq = 1000
amp = 1
phi = 0
offset = 0
x = np.arange(0, 120, 1 / sample_rate)
y = offset + amp * np.sin(2 * np.pi * freq * x + phi / 180 * np.pi)
# y = amp * np.ones(x.size)
# y = genSquareWave(sample_rate, freq, amp, 0.5, -amp / 2, 60)
# y = genSawtoothWave(sample_rate, freq, amp, -amp / 2, 60)
# y = genTriangleWave(sample_rate, freq, amp, 0.5, -amp / 2, 60)
# y = (np.arange(x.size) % 10) / 10
sd.default.device[1] = output_id
sd.play(y, sample_rate)
sd.wait()
