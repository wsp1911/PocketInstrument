import sounddevice as sd
import numpy as np
from pyaudio import PyAudio, paInt16


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
    x = np.arange(0, 1 / freq, 1 / sample_rate)
    y = offset + amp * np.sin(2 * np.pi * freq * x + phi / 180 * np.pi)
    return y


def genSquareWave(sample_rate, freq, amp, dutyRatio, offset):
    N = round(sample_rate / freq)
    x = np.arange(N)
    y = offset + amp * (x < dutyRatio * N)
    return y


def genSawtoothWave(sample_rate, freq, amp, offset):
    N = round(sample_rate / freq)
    N2 = 2
    y = np.r_[
        offset + np.linspace(0, amp, N - N2),
        np.linspace(amp + offset - amp / N2, offset, N2, endpoint=False),
    ]
    return y


def genTriangleWave(sample_rate, freq, amp, width, offset):
    N = round(sample_rate / freq)
    N1 = round(N * width)
    y = (
        offset
        + np.r_[
            np.linspace(0, amp, N1), np.linspace(0, amp, N - N1, endpoint=False)[::-1]
        ]
    )
    return y


def genDebugData():
    RATE = 44100
    amp = 0.5
    freq = 100
    t = 30
    N = int(t * RATE)
    y0 = amp * np.sin(2 * np.pi * freq * np.arange(0, t, 1 / RATE))
    # y1 = amp * np.cos(2 * np.pi * freq * np.arange(0, t, 1 / RATE))
    y1 = np.zeros(N)

    raw_data = np.zeros(N * 2)
    for i in range(N):
        raw_data[2 * i] = y0[i]
        raw_data[2 * i + 1] = y1[i]

    # return raw_data.astype(np.int16).tobytes()
    return (raw_data * 32768).astype(np.int16).tobytes()


output_id = get_output_device_id_by_name("扬声器 (EE Pocket Instrument)")
sample_rate = 44100
freq = 1000
amp = 0.5
phi = 0
offset = 0
x = np.arange(0, 120, 1 / sample_rate)
y = offset + amp * np.sin(2 * np.pi * freq * x + phi / 180 * np.pi)
# y = amp * np.ones(x.size)
# y = genSquareWave(sample_rate, freq, amp, 0.5, -amp / 2, 60)
# y = genSawtoothWave(sample_rate, freq, amp, -amp / 2, 60)
# y = genTriangleWave(sample_rate, freq, amp, 0.5, -amp / 2, 60)
# y = (np.arange(x.size) % 10) / 10

# sd.default.device[1] = output_id
# sd.play(y, sample_rate)
# sd.wait()


pa = PyAudio()
stream = pa.open(
    format=paInt16,
    channels=2,
    rate=44100,
    output=True,
)
y = genDebugData()
stream.write(y)
stream.stop_stream()
stream.close()
pa.terminate()
