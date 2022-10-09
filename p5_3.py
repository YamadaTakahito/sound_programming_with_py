import numpy as np
import soundfile as sf


def LPF(fs, fc, Q):
    fc /= fs
    fc = np.tan(np.pi * fc) / (2 * np.pi)
    a = np.zeros(3)
    b = np.zeros(3)
    a[0] = 1 + 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc
    a[1] = (8 * np.pi * np.pi * fc * fc - 2) / a[0]
    a[2] = (1 - 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc) / a[0]
    b[0] = 4 * np.pi * np.pi * fc * fc / a[0]
    b[1] = 8 * np.pi * np.pi * fc * fc / a[0]
    b[2] = 4 * np.pi * np.pi * fc * fc / a[0]
    a[0] = 1
    return a, b


s0, fs = sf.read("p5_3(input).wav")
length_of_s = len(s0)

s1 = np.zeros(length_of_s)
fc = 1000
Q = 1 / np.sqrt(2)
a, b = LPF(fs, fc, Q)
for n in range(length_of_s):
    for m in range(0, 3):
        if n - m >= 0:
            s1[n] += b[m] * s0[n - m]

    for m in range(1, 3):
        if n - m >= 0:
            s1[n] += -a[m] * s1[n - m]

sf.write("p5_3(output).wav", s1, fs)
