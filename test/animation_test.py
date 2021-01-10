import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
x, y = [], []
(line,) = plt.plot([], [], color="green")
nums = 100  # 需要的帧数


def init():
    ax.set_xlim(-5, 40)
    ax.set_ylim(-2, 2)
    return line


def update(step):
    x = np.linspace(0, 10 * np.pi, 1000)
    y = np.cos(1.2 * x + step)  # 这里只改变相位
    line.set_data(x, y)  # 设置新的 x，y
    return line


ani = FuncAnimation(
    fig,
    update,
    frames=nums,  # nums输入到frames后会使用range(nums)得到一系列step输入到update中去
    init_func=init,
    interval=100,
)
plt.show()
