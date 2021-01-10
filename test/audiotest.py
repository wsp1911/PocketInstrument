import wave
from pyaudio import PyAudio, paInt16
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024  # wav文件是由若干个CHUNK组成的，CHUNK我们就理解成数据包或者数据片段。
FORMAT = paInt16  # 表示我们使用量化位数 16位来进行录音
CHANNELS = 2  # 代表的是声道，1是单声道，2是双声道。
RATE = 44100  # 采样率 一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz,
# 11.025kHz, 22.05kHz, 44.1kHz。
RECORD_SECONDS = 0.1  # 录制时间这里设定了5秒


def save_wave_file(pa, filename, data):
    """save the date to the wavfile"""
    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    # wf.setsampwidth(sampwidth)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(data))
    wf.close()


def get_audio(filepath=None):
    isstart = str(input("是否开始录音？ （Y/N）"))  # 输出提示文本，input接收一个值,转为str，赋值给aa
    if isstart == "Y" or isstart == "y":
        pa = PyAudio()
        stream = pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        print("*" * 10, "开始录音：请在5秒内输入语音")
        frames = []  # 定义一个列表
        for i in range(
            0, int(RATE / CHUNK * RECORD_SECONDS)
        ):  # 循环，采样率 44100 / 1024 * 5
            data = stream.read(CHUNK)  # 读取chunk个字节 保存到data中
            # print(data)
            frames.append(data)  # 向列表frames中添加数据data
        # print(frames)
        print("*" * 10, "录音结束\n")

        stream.stop_stream()
        stream.close()  # 关闭
        pa.terminate()  # 终结

        if filepath is not None:
            save_wave_file(pa, filepath, frames)

        return b"".join(frames)
    elif isstart == "N" or isstart == "n":
        exit()
    else:
        print("无效输入，请重新选择")
        get_audio(filepath)


def display1(filepath):
    sampling_freq, audio = wavfile.read(filepath)
    audio = audio / (2.0 ** 15)
    x_values = np.arange(0, len(audio), 1) / float(sampling_freq)
    plt.figure()
    plt.plot(x_values, audio)


def display(data):
    L = len(data) // 4
    left, right = np.zeros(L), np.zeros(L)
    for i in range(L):
        left[i] = data[4 * i + 1] * 2 ** 8 + data[4 * i]
        right[i] = data[4 * i + 3] * 2 ** 8 + data[4 * i + 2]
    left /= 2.0 ** 15
    right /= 2.0 ** 15
    left = (left <= 1) * left + (left > 1) * (left - 2)
    right = (right <= 1) * right + (right > 1) * (right - 2)
    x = np.arange(0, L) / 44100
    plt.figure()
    plt.plot(x, left)
    plt.plot(x, right)


def play(filepath):
    wf = wave.open(filepath, "rb")
    p = PyAudio()
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )

    # 读数据
    data = wf.readframes(CHUNK)

    # 播放流
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()  # 暂停播放/录制
    stream.close()  # 终止播放

    p.terminate()  # 终止portaudio会话


if __name__ == "__main__":
    filepath = "test/01.wav"
    data = get_audio(filepath)
    print("Over!")
    display(data)
    display1(filepath)
    plt.show()
