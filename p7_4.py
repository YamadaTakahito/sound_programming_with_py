import numpy as np
import soundfile as sf


def LSF(fs, fc, Q, g):
    fc /= fs
    fc = np.tan(np.pi * fc) / (2 * np.pi)
    a = np.zeros(3)
    b = np.zeros(3)
    a[0] = 1 + 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc
    a[1] = (8 * np.pi * np.pi * fc * fc - 2) / a[0]
    a[2] = (1 - 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc) / a[0]
    b[0] = (1 + 2 * np.pi * fc / Q * np.sqrt(1 + g) + 4 * np.pi * np.pi * fc * fc * (1 + g)) / a[0]
    b[1] = (8 * np.pi * np.pi * fc * fc * (1 + g) - 2) / a[0]
    b[2] = (1 - 2 * np.pi * fc / Q * np.sqrt(1 + g) + 4 * np.pi * np.pi * fc * fc * (1 + g)) / a[0]
    a[0] = 1
    return a, b


def HSF(fs, fc, Q, g):
    fc /= fs
    fc = np.tan(np.pi * fc) / (2 * np.pi)
    a = np.zeros(3)
    b = np.zeros(3)
    a[0] = 1 + 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc
    a[1] = (8 * np.pi * np.pi * fc * fc - 2) / a[0]
    a[2] = (1 - 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc) / a[0]
    b[0] = (1 + g + 2 * np.pi * fc / Q * np.sqrt(1 + g) + 4 * np.pi * np.pi * fc * fc) / a[0]
    b[1] = (8 * np.pi * np.pi * fc * fc - 2 * (1 + g)) / a[0]
    b[2] = (1 + g - 2 * np.pi * fc / Q * np.sqrt(1 + g) + 4 * np.pi * np.pi * fc * fc) / a[0]
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


def PF(fs, fc, Q, g):
    fc /= fs
    fc = np.tan(np.pi * fc) / (2 * np.pi)
    a = np.zeros(3)
    b = np.zeros(3)
    a[0] = 1 + 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc
    a[1] = (8 * np.pi * np.pi * fc * fc - 2) / a[0]
    a[2] = (1 - 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc) / a[0]
    b[0] = (1 + 2 * np.pi * fc / Q * (1 + g) + 4 * np.pi * np.pi * fc * fc) / a[0]
    b[1] = (8 * np.pi * np.pi * fc * fc - 2) / a[0]
    b[2] = (1 - 2 * np.pi * fc / Q * (1 + g) + 4 * np.pi * np.pi * fc * fc) / a[0]
    a[0] = 1
    return a, b


s0, fs = sf.read("p7_4(input).wav")

fc = 500
Q = 1 / np.sqrt(2)
g = -1
a, b = LSF(fs, fc, Q, g)
s1 = filter(a, b, s0)

s0 = s1

fc = 1000
Q = 1 / np.sqrt(2)
g = 1
a, b = PF(fs, fc, Q, g)
s1 = filter(a, b, s0)

s0 = s1
fc = 2000
Q = 1 / np.sqrt(2)
g = -1
a, b = HSF(fs, fc, Q, g)
s1 = filter(a, b, s0)

master_volume = 1
s1 /= np.max(np.abs(s1))
s1 *= master_volume

sf.write("p7_4(output).wav", s1.copy(), fs)
