import numpy as np
from matplotlib import pyplot as plt


def ADSR(fs, A, D, S, R, gate, duration):
    A = int(fs * A)
    D = int(fs * D)
    R = int(fs * R)
    gate = int(fs * gate)
    duration = int(fs * duration)
    e = np.zeros(duration)

    if A != 0:
        for n in range(A):
            e[n] = (1 - np.exp(-5 * n / A)) / (1 - np.exp(-5))
    if D != 0:
        for n in range(A, gate):
            e[n] = 1 + (S - 1) * (1 - np.exp(-5 * (n - A) / D))
    else:
        for n in range(A, gate):
            e[n] = S
    if R != 0:
        for n in range(gate, duration):
            e[n] = e[gate - 1] - e[gate - 1] * (1 - np.exp(-5 * (n - gate + 1) / R))
    return e


fs = 44100

A = 0.1
D = 0.4
S = 0.5
R = 0.4
gate = 1
duration = 2
offset = 0
depth = 1

length_of_s = int(fs * duration)

e = ADSR(fs, A, D, S, R, gate, duration)
for n in range(length_of_s):
    e[n] = offset + e[n] * depth

t = np.zeros(length_of_s)
for n in range(length_of_s):
    t[n] = n / fs

plt.figure()
plt.plot(t, e)
plt.axis([0, 2, 0, 1])
plt.xlabel("time[s]")
plt.ylabel("amlitude")
plt.savefig("p6_5.png")
plt.show()
