"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import pyaudio
import time
import numpy as np
import matplotlib.pyplot as plt


def get_chunk(f, RATE):
    if f == 0:
        return 1024
    N = int(RATE / f)
    chunk = 2 ** int(np.log2(N * 6) + 1)
    return max(chunk, 1024)


WIDTH = 2
CHANNELS = 2
RATE = 44100
global pos
pos = 0
f = 0
CHUNK = get_chunk(f, RATE)
print(CHUNK)
t = np.arange(0, CHUNK / RATE, 1 / RATE)
global y
# y1 = 0.5 * np.sin(2 * np.pi * f * t)
# y2 = 0.5 * np.sin(2 * np.pi * f * t)
y = 0.5 * np.ones(CHUNK)
y = np.repeat(y, 2)
y = (-y * 32768).astype(np.int16).tobytes()
global rec_y
rec_y = bytes()
global cnt
cnt = 0


p = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    global y, rec_y, cnt
    data = y
    rec_y += in_data
    return (data, pyaudio.paContinue)


stream = p.open(
    format=p.get_format_from_width(WIDTH),
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    stream_callback=callback,
    frames_per_buffer=CHUNK,
)

stream.start_stream()

L_reg = 0
while cnt < 2:
    rec_y_copy = rec_y
    if len(rec_y_copy) >= CHUNK * 4:
        rec_data = np.fromstring(rec_y_copy[-4 * CHUNK :], dtype=np.int16) / 32768
        if np.max(rec_data) > 0.02 and L_reg != len(rec_y_copy):
            L_reg = len(rec_y_copy)
            cnt += 1

print(cnt)

# while stream.is_active():
#     time.sleep(0.1)
# t1 = time.perf_counter()
# t2 = t1
# while t2 - t1 < 10 * CHUNK / RATE:
#     t2 = time.perf_counter()

# print("time: %f" % (time.perf_counter() - t1))

stream.stop_stream()
stream.close()

p.terminate()

rec_y = np.fromstring(rec_y, dtype=np.int16) / 32768
y11 = rec_y[::2]
y22 = rec_y[1::2]

# for i in range(1, len(y1)):
#     if abs(y1[i] - y1[i - 1]) > 0.1:
#         print("%d %f %f" % (i, y1[i], y1[i - 1]))
M, N = 2, 1
# plt.subplot(M, N, 1)
# plt.plot(y1)
plt.subplot(M, N, 1)
plt.plot(y11)
# plt.subplot(M, N, 3)
# plt.plot(y2)
plt.subplot(M, N, 2)
plt.plot(y11)
plt.plot(y22)
plt.show()

np.save("y_%d.npy" % f, (y11, y22))
