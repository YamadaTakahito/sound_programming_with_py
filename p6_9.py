import numpy as np
import soundfile as sf


def HPF(fs, fc, Q):
    fc /= fs
    fc = np.tan(np.pi * fc) / (2 * np.pi)
    a = np.zeros(3)
    b = np.zeros(3)
    a[0] = 1 + 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc;
    a[1] = (8 * np.pi * np.pi * fc * fc - 2) / a[0]
    a[2] = (1 - 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc) / a[0]
    b[0] = 1 / a[0]
    b[1] = -2 / a[0]
    b[2] = 1 / a[0]
    a[0] = 1
    return a, b


def filter(a, b, x):
    length_of_x = len(x)
    y = np.zeros(length_of_x)
    for n in range(length_of_x):
        for m in range(0, 3):
            if n - m >= 0:
                y[n] += b[m] * x[n - m]

        for m in range(1, 3):
            if n - m >= 0:
                y[n] += -a[m] * y[n - m]

    return y


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
f0 = 440

gate = 3
duration = 4

decay = 8
d = 0.5

T = 1 / f0

num = np.power(10, -3 * T / decay)
den = np.sqrt((1 - d) * (1 - d) + 2 * d * (1 - d) * np.cos((2 * np.pi * f0) / fs) + d * d)

c = num / den

if c > 1:
    c = 1

D = int(T * fs - d)
e = T * fs - d - int(T * fs - d)
g = (1 - e) / (1 + e)

length_of_s = int(fs * duration)
s0 = np.zeros(length_of_s)
s1 = np.zeros(length_of_s)
s2 = np.zeros(length_of_s)

np.random.seed(0)
mean_of_s0 = 0
for n in range(D + 1):
    s0[n] = (np.random.rand() * 2) - 1
    mean_of_s0 += s0[n]

mean_of_s0 /= D + 1
for n in range(D + 1):
    s0[n] -= mean_of_s0

for n in range(D + 1, length_of_s):
    s1[n] = -g * s1[n - 1] + g * s0[n - D] + s0[n - D - 1]

    s2[n] = c * ((1 - d) * s1[n] + d * s1[n - 1])

    s0[n] += s2[n]

fc = 5
Q = 1 / np.sqrt(2)
a, b = HPF(fs, fc, Q)
s3 = filter(a, b, s0)

VCA_A = np.array([0])
VCA_D = np.array([0])
VCA_S = np.array([1])
VCA_R = np.array([0.1])
VCA_gate = np.array([gate])
VCA_duration = np.array([duration])
VCA_offset = np.array([0])
VCA_depth = np.array([1])

vca = ADSR(fs, VCA_A[0], VCA_D[0], VCA_S[0], VCA_R[0], VCA_gate[0], VCA_duration[0])
for n in range(length_of_s):
    vca[n] = VCA_offset[0] + vca[n] * VCA_depth[0]

for n in range(length_of_s):
    s3[n] *= vca[n]

length_of_s_master = int(fs * (duration + 2))
s_master = np.zeros(length_of_s_master)

offset = int(fs * 1)
for n in range(length_of_s):
    s_master[offset + n] += s3[n]

master_volume = 0.5
s_master /= np.max(np.abs(s_master))
s_master *= master_volume

sf.write("p6_9(output).wav", s_master, fs)
