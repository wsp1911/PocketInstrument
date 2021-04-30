import numpy as np

A1, A2 = 2, 3
phi1, phi2 = np.pi / 2, np.pi / 4
d_phi = phi1 - phi2
f = 10000
df = 1 / 44100
N = 100
t = np.arange(0, N / f, df)
y1 = A1 * np.sin(2 * np.pi * f * t + phi1)
y2 = A2 * np.sin(2 * np.pi * f * t + phi2)

s1 = np.sin(2 * np.pi * f * t)
s2 = np.cos(2 * np.pi * f * t)

y10 = np.sum(y1 * s1 * df) * 2 * f / N
y11 = np.sum(y1 * s2 * df) * 2 * f / N
y20 = np.sum(y2 * s1 * df) * 2 * f / N
y21 = np.sum(y2 * s2 * df) * 2 * f / N

A11 = np.sqrt(y10 ** 2 + y11 ** 2)
A21 = np.sqrt(y20 ** 2 + y21 ** 2)
phi11 = np.arccos(y10 / A11)
phi21 = np.arccos(y20 / A21)
d_phi1 = phi11 - phi21

print("A=%f, phi=%f\nA1=%f, phi=%f" % (A1 / A2, d_phi, A11 / A21, d_phi1))
