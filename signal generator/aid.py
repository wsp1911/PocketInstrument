# import numpy as np
# import matplotlib.pyplot as plt

# f = np.array([500, 1e3, 2e3, 3e3, 5e3, 7e3, 10e3, 13e3, 16e3, 20e3])
# dphi = np.array([1, 4, 7, 10, 19, 26, 37, 48, 60, 75])

# plt.plot(f, dphi)
# plt.show()


# def play(threadName, delay):
#     chunk = 1024  # 2014kb
#     p = PyAudio()
#     stream = p.open(
#         format=p.get_format_from_width(sampwidth),
#         channels=channel,
#         rate=framerate,
#         output=True,
#     )

#     while outing == 1:
#         count = 0
#         wf = d_data
#         data = wf[0:chunk]
#         while data != b"":  # 播放
#             stream.write(data)
#             count = count + 1
#             data = wf[count * chunk : (count + 1) * chunk]
#     stream.stop_stream()  # 停止数据流
#     stream.close()
#     p.terminate()  # 关闭 PyAudio


def NOT(s):
    res = []
    for each in s[2:]:
        res.append("1" if each == "0" else "0")
    s = "".join(res)
    if len(s) < 8:
        s = "1" * (8 - len(s)) + s
    return "0b" + s


def dec2hex(n):
    if n >= 0:
        return hex(n) + "00"
    else:
        return hex(int(NOT(bin(-n)), 2) + 1) + "00"


print(dec2hex(8))
