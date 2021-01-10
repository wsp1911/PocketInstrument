import numpy as np
import matplotlib.pyplot as plt
import wave
import math
from pyaudio import *
import tkinter as tk
import _thread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


def sin_wave(A=0.5, f=100, fs=44100, t=1):  # 正弦波
    """
    :params A:    振幅
    :params f:    信号频率
    :params fs:   采样频率
    :params t:    时间长度
    """
    # 若时间序列长度为 t=1s,
    # 采样频率 fs=1000 Hz, 则采样时间间隔 Ts=1/fs=0.001s
    # 对于时间序列采样点个数为 n=t/Ts=1/0.001=1000, 即有1000个点,每个点间隔为 Ts
    Ts = 1 / fs
    n = t / Ts
    n = np.arange(n)
    y = A * np.sin(2 * np.pi * f * n * Ts)

    return y


def triangle_wave(A=0.5, f=100, fs=44100, t=1):
    """
    :params A:    振幅
    :params f:    信号频率
    :params fs:   采样频率
    :params t:    时间长度
    """
    n = t * fs
    T = 1 / f  # 周期
    n = np.arange(n)
    Ts = 1 / fs
    t = np.zeros(len(n))
    t[0] = -1 * A
    for i in range(len(n)):
        time = n[i] * Ts  # 当前时间
        La = int(time / (0.5 * T))  # 距现在最近的上个拐点
        if La % 2 == 0:  # 如果正在上升
            t[i] = -A + (time - La * 0.5 * T) * 2 * A / 0.5 / T
        else:
            t[i] = A - (time - La * 0.5 * T) * 2 * A / 0.5 / T
    return t


def swatooth_wave(A=0.5, f=100, fs=44100, t=1):
    """
    :params A:    振幅
    :params f:    信号频率
    :params fs:   采样频率
    :params t:    时间长度
    """
    n = t * fs
    T = 1 / f  # 周期
    n = np.arange(n)
    Ts = 1 / fs
    t = np.zeros(len(n))
    t[0] = -1 * A
    for i in range(len(n)):
        time = n[i] * Ts  # 当前时间
        La = int(time / T)  # 距现在最近的上个周期
        t[i] = -A + (time - La * T) * 2 * A / T
    return t


def rect_square_wave(A=0.5, f=100, fs=44100, t=1, duty=0.5):  # 方波
    """
    :params A:    振幅
    :params f:    信号频率
    :params fs:   采样频率
    :params t:    时间长度

    Returns
    -------

    """

    Ts = 1 / fs
    n = t / Ts
    n = np.arange(n)
    d = np.zeros_like(n)
    tnum = fs / f
    for i in range(len(n)):
        if i % tnum / tnum <= duty:
            d[i] = A

        else:
            d[i] = -A
    return d


def play(threadName, delay):
    chunk = 1024  # 2014kb
    p = PyAudio()
    stream = p.open(
        format=p.get_format_from_width(sampwidth),
        channels=channel,
        rate=framerate,
        output=True,
    )

    while outing == 1:
        count = 0
        wf = d_data
        data = wf[0:chunk]
        while data != b"":  # 播放
            stream.write(data)
            count = count + 1
            data = wf[count * chunk : (count + 1) * chunk]
    stream.stop_stream()  # 停止数据流
    stream.close()
    p.terminate()  # 关闭 PyAudio


def Output():
    global outing
    outing = 1
    Wavedic = {1: "正弦波", 2: "方波", 3: "锯齿波", 4: "三角波", 5: "无"}
    if Wavevar.get() == 5 & Wavevar2.get() == 5:
        print("无输出")
        return

    if Wavevar.get() != 5:
        if (Fretext.get() == "") | (Peaktext.get() == ""):
            print("请正确输入频率和峰值！")
            return

        Freq = float(Fretext.get())
        Peak = float(Peaktext.get())
        DC = float(DCtext.get()) / 20
        Duty = float(Dutytext.get())
        Wavetype = Wavedic[Wavevar.get()]
        print(
            "通道一：",
            Wavetype,
            "频率是：",
            Freq,
            "Hz,峰值是:",
            Peak,
            "V，占空比：",
            Duty,
            "直流分量：",
            DC,
            "V",
        )
    else:
        Freq = -1
        print("通道一：关闭")

    if Wavevar2.get() != 5:
        if (Fretext2.get() == "") | (Peaktext2.get() == ""):
            print("请正确输入频率和峰值！")
            return
        Freq2 = float(Fretext2.get())
        Peak2 = float(Peaktext2.get())
        Wavetype2 = Wavedic[Wavevar2.get()]
        DC2 = float(DCtext2.get()) / 20
        Duty2 = float(Dutytext2.get())
        print(
            "通道二：",
            Wavetype2,
            "频率是：",
            Freq2,
            "Hz,峰值是:",
            Peak2,
            "V，占空比：",
            Duty2,
            "直流分量：",
            DC2,
            "V",
        )
    else:
        Freq2 = -1
        print("通道二：关闭")

    if Wavevar.get() == 1:
        d = np.array(sin_wave(A=Peak / 20, f=Freq, fs=44100, t=10 / Freq))  # 正弦波
    elif Wavevar.get() == 2:
        d = np.array(
            rect_square_wave(A=Peak / 20, f=Freq, fs=44100, t=10 / Freq, duty=Duty)
        )  # 方波
    elif Wavevar.get() == 3:
        d = np.array(swatooth_wave(A=Peak / 20, f=Freq, fs=44100, t=10 / Freq))  # 锯齿波
    elif Wavevar.get() == 4:
        d = np.array(triangle_wave(A=Peak / 20, f=Freq, fs=44100, t=10 / Freq))  # 三角波
    elif Wavevar.get() == 5:
        d = 0
    else:
        print("Wave Error! Wavetype is", Wavetype)
        return

    if Wavevar2.get() == 1:
        d2 = np.array(sin_wave(A=Peak2 / 20, f=Freq2, fs=44100, t=10 / Freq))  # 正弦波
    elif Wavevar2.get() == 2:
        d2 = np.array(
            rect_square_wave(A=Peak2 / 20, f=Freq2, fs=44100, t=10 / Freq2, duty=Duty2)
        )  # 方波
    elif Wavevar2.get() == 3:
        d2 = np.array(
            swatooth_wave(A=Peak2 / 20, f=Freq2, fs=44100, t=10 / Freq)
        )  # 锯齿波
    elif Wavevar2.get() == 4:
        d2 = np.array(
            triangle_wave(A=Peak2 / 20, f=Freq2, fs=44100, t=10 / Freq)
        )  # 三角波
    elif Wavevar2.get() == 5:
        d2 = 0
    else:
        print("Wave Error! Wavetype is", Wavetype)
        return

    if Freq == -1:
        out = d2 + DC2
    elif Freq2 == -1:
        out = d + DC
    else:
        num = 0
        out = np.zeros(2 * len(d))
        for i in d:
            out[2 * num] = i + DC
            out[2 * num + 1] = d2[num] + DC2
            num += 1

        plt.plot(d[:500])  # 画出波形图(改)
        plt.show()
        plt.plot(d2[:500])  # 画出波形图(改)
        plt.show()
    plt.plot(out[:50000])  # 画出波形图(改)
    plt.show()
    # print(out)
    file = wave.open(r"hello.wav", "wb")
    global channel
    global sampwidth
    global framerate
    if (Freq == -1) | (Freq2 == -1):
        file.setnchannels(1)  # 设置通道数
        channel = 1
    else:
        file.setnchannels(2)  # 设置通道数
        channel = 2
    file.setsampwidth(2)  # 设置采样宽
    sampwidth = 2
    file.setframerate(44100)  # 设置采样
    framerate = 44100
    file.setcomptype("NONE", "not compressed")  # 设置采样格式  无压缩
    d1 = out * 32768  # 播放音频（改）
    global d_data
    d_data = d1.astype(np.int16).tobytes()
    # file.writeframes(d_data)
    file.close()
    # print("Outing is ",outing)
    try:
        _thread.start_new_thread(
            play,
            (
                "Thread-1",
                2,
            ),
        )
    except:
        print("Error: 无法启动线程")


def Outputend():
    global outing
    outing = 0
    print("end!")


def test(content):  # 仅数字
    # 如果不加上==""的话，就会发现删不完。总会剩下一个数字
    if (
        content.replace(".", "").replace("-", "").isdigit()
        or content == ""
        or content == "-"
    ):
        return True
    else:
        return False


print("hello there")
outing = 0
top = tk.Tk()
top.title("信号发生器")  # 标题
top.geometry("600x500")  # 窗口尺寸

lab1 = tk.Label(top, text="频率：", width=5, height=1)
lab1.place(x=150, y=120)
lab2 = tk.Label(top, text="频率：", width=5, height=1)
lab2.place(x=350, y=120)

lab4 = tk.Label(top, text="占空比：", width=10, height=1)
lab4.place(x=130, y=180)
lab42 = tk.Label(top, text="占空比：", width=10, height=1)
lab42.place(x=330, y=180)

lab5 = tk.Label(top, text="直流分量：", width=10, height=1)
lab5.place(x=120, y=210)
lab52 = tk.Label(top, text="直流分量：", width=10, height=1)
lab52.place(x=320, y=210)
# bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
# l.pack()

lab2 = tk.Label(top, text="选择输出波形：", width=14, height=1)
lab2.place(x=100, y=10)

lab22 = tk.Label(top, text="选择输出波形：", width=14, height=1)
lab22.place(x=300, y=10)

lab3 = tk.Label(top, text="峰值：", width=5, height=1)
lab3.place(x=150, y=150)
lab32 = tk.Label(top, text="峰值：", width=5, height=1)
lab32.place(x=350, y=150)

Wavevar = tk.IntVar()
Wavevar.set(5)
r1 = tk.Radiobutton(top, text="正弦波", variable=Wavevar, value="1")
r1.place(x=200, y=10)
r2 = tk.Radiobutton(top, text="方波", variable=Wavevar, value="2")
r2.place(x=200, y=30)
r3 = tk.Radiobutton(top, text="锯齿波", variable=Wavevar, value="3")
r3.place(x=200, y=50)
r4 = tk.Radiobutton(top, text="三角波", variable=Wavevar, value="4")
r4.place(x=200, y=70)
r5 = tk.Radiobutton(top, text="关闭", variable=Wavevar, value="5")
r5.place(x=200, y=90)

Wavevar2 = tk.IntVar()
Wavevar2.set(5)
r12 = tk.Radiobutton(top, text="正弦波", variable=Wavevar2, value="1")
r12.place(x=400, y=10)
r22 = tk.Radiobutton(top, text="方波", variable=Wavevar2, value="2")
r22.place(x=400, y=30)
r32 = tk.Radiobutton(top, text="锯齿波", variable=Wavevar2, value="3")
r32.place(x=400, y=50)
r42 = tk.Radiobutton(top, text="三角波", variable=Wavevar2, value="4")
r42.place(x=400, y=70)
r52 = tk.Radiobutton(top, text="关闭", variable=Wavevar2, value="5")
r52.place(x=400, y=90)

test_cmd = top.register(test)  # 需要将函数包装一下，必要的
Fretext = tk.StringVar()
Freinput = tk.Entry(
    top,
    textvariable=Fretext,
    font=("Arial", 14),
    width=5,
    validate="key",  # 发生任何变动的时候，就会调用validatecommand
    validatecommand=(test_cmd, "%P"),
)  # %P代表输入框的实时内容)        #输入频率

Fretext2 = tk.StringVar()
Freinput2 = tk.Entry(
    top,
    textvariable=Fretext2,
    font=("Arial", 14),
    width=5,
    validate="key",  # 发生任何变动的时候，就会调用validatecommand
    validatecommand=(test_cmd, "%P"),
)  # %P代表输入框的实时内容)        #输入频率
Freinput.place(x=200, y=120)
Freinput2.place(x=400, y=120)


# 当validate为key的时候，获取输入框内容就不可以用get（）
# 只有当validatecommand判断正确后，返回true。才会改变.get()返回的值.所以要用%P

Peaktext = tk.StringVar()
Peakinput = tk.Entry(
    top,
    textvariable=Peaktext,
    font=("Arial", 14),
    width=5,
    validate="key",  # 发生任何变动的时候，就会调用validatecommand
    validatecommand=(test_cmd, "%P"),
)  # %P代表输入框的实时内容)        #输入峰值电压

Peaktext2 = tk.StringVar()
Peakinput2 = tk.Entry(
    top,
    textvariable=Peaktext2,
    font=("Arial", 14),
    width=5,
    validate="key",  # 发生任何变动的时候，就会调用validatecommand
    validatecommand=(test_cmd, "%P"),
)  # %P代表输入框的实时内容)        #输入峰值电压
Peakinput.place(x=200, y=150)
Peakinput2.place(x=400, y=150)


Dutytext = tk.StringVar()
Dutytext.set("0.5")
Dutyinput = tk.Entry(
    top,
    textvariable=Dutytext,
    font=("Arial", 14),
    width=5,
    validate="key",  # 发生任何变动的时候，就会调用validatecommand
    validatecommand=(test_cmd, "%P"),
)  # %P代表输入框的实时内容)        #输入占空比

Dutytext2 = tk.StringVar()
Dutytext2.set("0.5")
Dutyinput2 = tk.Entry(
    top,
    textvariable=Dutytext2,
    font=("Arial", 14),
    width=5,
    validate="key",  # 发生任何变动的时候，就会调用validatecommand
    validatecommand=(test_cmd, "%P"),
)  # %P代表输入框的实时内容)        #输入占空比
Dutyinput.place(x=200, y=180)
Dutyinput2.place(x=400, y=180)


DCtext = tk.StringVar()
DCtext.set("0")
DCinput = tk.Entry(
    top,
    textvariable=DCtext,
    font=("Arial", 14),
    width=5,
    validate="key",  # 发生任何变动的时候，就会调用validatecommand
    validatecommand=(test_cmd, "%P"),
)  # %P代表输入框的实时内容)        #输入直流分量

DCtext2 = tk.StringVar()
DCtext2.set("0")
DCinput2 = tk.Entry(
    top,
    textvariable=DCtext2,
    font=("Arial", 14),
    width=5,
    validate="key",  # 发生任何变动的时候，就会调用validatecommand
    validatecommand=(test_cmd, "%P"),
)  # %P代表输入框的实时内容)        #输入直流分量
DCinput.place(x=200, y=210)
DCinput2.place(x=400, y=210)


def StartOutput(even):
    Output()


Outputbutton = tk.Button(top, text="开始输出", command=Output)
top.bind("<Return>", StartOutput)
Outputbutton.place(x=180, y=280)
Outputendbutton = tk.Button(top, text="结束输出", command=Outputend)
Outputendbutton.place(x=180, y=320)


# def key(event):
#    print("pressed", repr(event.char))

# def callback(event):
#   frame.focus_set()
#   print("clicked at", event.x, event.y)

# frame = tk.Frame(top, width=100, height=100)
# frame.bind("<Key>", key)
# frame.bind("<Button-1>", callback)
# frame.pack()
def CloseWindow(even):
    top.destroy()


top.bind("<Escape>", CloseWindow)

Ordertext = tk.StringVar()
Orderinput = tk.Entry(
    top,
    textvariable=Ordertext,
    font=("Arial", 14),
    width=15,
    validate="key",  # 发生任何变动的时候，就会调用validatecommand
)  # %P代表输入框的实时内容)        #输入占空比
Orderinput.place(x=370, y=280)


def RunOrder():
    global outing
    outing = 1
    order = Ordertext.get()
    global d_data
    out = eval(order)
    d1 = out * 32768  # 播放音频（改）
    d_data = d1.astype(np.int16).tobytes()
    global channel
    global sampwidth
    global framerate
    channel = 1
    sampwidth = 2
    framerate = 44100
    try:
        _thread.start_new_thread(
            play,
            (
                "Thread-1",
                2,
            ),
        )
    except:
        print("Error: 无法启动线程")


RunOrderbutton = tk.Button(top, text="执行", command=RunOrder)
RunOrderbutton.place(x=550, y=280)
top.mainloop()