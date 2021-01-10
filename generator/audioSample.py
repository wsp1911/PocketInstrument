import os
import sys
import time
import wave
import numpy as np
import array
import sounddevice as sd
from scipy.io import wavfile
import soundfile


class MyException(Exception):
    """
    自定义的异常类
    """

    def __init__(self, *args):
        self.args = args


def preliminary_instruction():
    """
    初步介绍 sounddevice 查询声卡相关操作
    :return:
    """
    # 首先获取与当前主机连接的声卡设备驱动信息
    drivers_tuple = sd.query_hostapis()
    print(drivers_tuple)  # 返回一个包含声卡驱动信息的元组, 元组的每个元素, 是一个个字典, 包含了每个驱动的详细信息

    for driver_msg_dict in drivers_tuple:
        # 能够获取每个驱动的名字
        print(
            driver_msg_dict["name"], end=", "
        )  # MME, Windows DirectSound, ASIO, Windows WASAPI, Windows WDM-KS,

    # 查询当前主机能用的声卡声道
    devices_list = sd.query_devices()  # 返回一个列表

    # 每个设备信息, 以字典形式呈现
    for device_msg_dict in devices_list:
        print(device_msg_dict)


# 下面两个函数, 是根据声卡声道名字, 获取声卡声道名称 及 id, 区分 输出 和 输入 两种声道
def get_input_device_id_by_name(channel_name):
    """
    功能: 根据声卡声道名字, 获取 输入 声道 id
    :return: 返回输入声道id
    """

    devices_list = sd.query_devices()
    for index, device_msg_dict in enumerate(devices_list):
        if (
            channel_name == device_msg_dict["name"]
            and device_msg_dict["max_input_channels"] > 0
        ):
            return index
    else:
        raise MyException("找不到该设备!!!")


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
        raise MyException("找不到该设备!!!")


def read_data(audio_file_path, audio_channels):
    # wav格式文件与 raw(pcm) 格式区分开, 不同格式, 获取其数据内容的方式不一样
    if audio_file_path.endswith(".wav"):
        data_array, sample_rate = soundfile.read(audio_file_path)
        return data_array

    elif audio_file_path.endswith(".pcm") or audio_file_path.endswith(".raw"):
        # 打开一个音频文件, 以 raw(pcm) 格式为例
        data_array = array.array("h")
        with open(audio_file_path, "rb") as f:
            data_array.frombytes(f.read())

        # 根据声道数, 来进行切分(我用的音频是双声道)
        data_array = data_array[::audio_channels]  # 有几个声道, 切分的步长就是几, 这样就能单独切出来一个声道
        return data_array


def play_audio_file(audio_file_path, channel_id, audio_channels, sample_rate):

    # 将本机默认的输出声道, 改为 自己设定的声道
    # sd.default.device 是一个列表, 第一个元素是: 默认的输入设备id;    第二个是默认的输出设备id
    sd.default.device[1] = channel_id

    # 常选参数, 一个数据, 一个采样率, 另外还有一个: blocking=True, 若设置, 则表示播放完毕当前音频再往下进行程序
    data_array = read_data(audio_file_path, audio_channels)
    sd.play(data_array, sample_rate)
    sd.wait()  # 表示等到此音频文件播放完毕之后再往下进行程序
    # time.sleep(20)  # 使用 time.sleep() ---> 休眠几秒, 音频文件就播放几秒, 时长自己控制

    # 注: 如果没有 类似休眠 等延时操作, 则程序只会一闪而过, 不会播放音频


# 使用 sounddevice_example 录制音频, 提示也可以用多进程
def do_record(channel_id, file_path):
    # 首先设置默认录音声道id, id不同, 调用的录音声卡也会不同, 和 播放一样, 也支持 多进程+多线程, 多个声道同时录音
    sd.default.device[0] = channel_id

    # 再调用函数录音
    sample_rate = 44100  # 音频采样率
    length = 10  # 时长, 单位秒
    record_data = sd.rec(
        frames=length * sample_rate, samplerate=sample_rate, channels=1, blocking=True
    )  # blocking=True, 能够让录音直到时长

    wavfile.write(file_path, sample_rate, record_data)


# 边录边播
def play_and_record(
    input_channel_id,
    output_channel_id,
    play_audio_file_path,
    rec_file_path,
    play_audio_channels=1,
    play_audio_fs=44100,
    rec_file_channels=1,
):

    # 首先设置默认输出和输入声道
    sd.default.device[0] = input_channel_id
    sd.default.device[1] = output_channel_id

    # 开始边录边播
    data_array = read_data(play_audio_file_path, play_audio_channels)
    rec_data = sd.playrec(
        data=data_array,
        samplerate=play_audio_fs,
        channels=rec_file_channels,
        blocking=True,
    )

    # 存储录音文件
    wavfile.write(rec_file_path, play_audio_fs, rec_data)


# if __name__ == "__main__":
#     preliminary_instruction()
#     # file_path = r"F:\CloudMusic\download\FIRBetterLife.raw"
#     file_path = r"F:\CloudMusic\download\EpicScoreFireHead.raw"
#     output_id = get_output_device_id_by_name(
#         "喇叭/耳机 (Realtek High Definition Audio(SST))"
#     )
#     rec_file_path = os.getcwd() + "\\test_record.wav"
#     input_id = get_input_device_id_by_name("扬声器 (UTC Audio Device)")

#     # play_audio_file(rec_file_path, output_id, 1, 44100)  # 只播放
#     # do_record(channel_id, file_path)  # 只录音

#     # play_and_record(input_id, output_id, file_path, rec_file_path, play_audio_channels=2)  # 边录边播

#     # file_path = sys.argv[1]
#     # output_id = int(sys.argv[2])
#     # audio_channels = int(sys.argv[3])
#     # fs = int(sys.argv[4])
#     # play_audio_file(file_path, output_id, audio_channels, fs)  # 接收shell参数, 多进程多声道播放音乐

# if __name__ == "__main__":
#     # preliminary_instruction()
#     output_id = get_output_device_id_by_name("扬声器 (UTC Audio Device)")
#     sample_rate = 44100
#     x = np.arange(0, 10, 1 / sample_rate)
#     i = np.arange(0, x.size)
#     y = np.sin(2 * np.pi * 1000 * x)
#     # y = np.array(i % 200 < 100, dtype=np.float64)
#     # y = np.ones(x.size, dtype=np.float64)
#     sd.default.device[1] = output_id
#     sd.play(y, sample_rate)
#     sd.wait()

# def find_sine_pks(x,freq):


def find_sine_pks1(x):
    s, e = [], []
    for i in range(1, x.size):
        if x[i] * x[i - 1] <= 0 and x[i - 1] != 0:
            if x[i] > x[i - 1]:
                s.append(i)
            else:
                e.append(i)
    i = j = 0
    maxs, mins = [], []
    while i < len(s) and j < len(e):
        if s[i] < e[j]:
            maxs.append(np.max(x[s[i] : e[j]]))
            i += 1
        else:
            mins.append(np.min(x[e[j] : s[i]]))
            j += 1
    return np.mean(np.array(maxs)), np.mean(np.array(mins))


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.ion()

    channel_id = get_input_device_id_by_name("麦克风 (EE Pocket Instrument)")

    sd.default.device[0] = channel_id

    # 再调用函数录音
    sample_rate = 44100  # 音频采样率
    length = 0.01  # 时长, 单位秒
    t = np.linspace(0, length, int(sample_rate * length))
    while True:
        record_data = sd.rec(
            frames=int(length * sample_rate),
            samplerate=sample_rate,
            channels=1,
            blocking=True,
        )  # blocking=True, 能够让录音直到时长
        plt.cla()
        record_data = np.ravel(record_data)
        record_data *= 6.4 / 0.8475
        plt.plot(t, record_data)
        # vmax, vmin = find_sine_pks(record_data)
        # vmax, vmin = round(vmax, 4), round(vmin, 4)
        vmax = round(np.max(record_data), 4)
        vmin = round(np.min(record_data), 4)
        vmean = round(np.mean(record_data), 4)
        plt.title(
            "min="
            + str(vmin)
            + ", max="
            + str(vmax)
            + ", Vpp="
            + str(round(vmax - vmin, 4))
            + ", mean="
            + str(vmean)
        )
        plt.pause(0.2)
