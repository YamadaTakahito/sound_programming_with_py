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


def distortion(fs, gain, level, x):
    length_of_x = len(x)
    y = np.zeros(length_of_x)

    fc = 200
    Q = 1 / np.sqrt(2)
    a, b = LPF(fs, fc, Q)
    u0 = filter(a, b, x)

    ratio = 4

    u1 = np.zeros(length_of_x * ratio)
    for n in range(length_of_x):
        u1[(n - 1) * ratio] = u0[n]

    fc = 20000 / ratio
    Q = 1 / np.sqrt(2)

    a, b = LPF(fs, fc, Q)
    u2 = filter(a, b, u1)

    u3 = np.zeros(length_of_x * ratio)
    for n in range(length_of_x * ratio):
        u3[n] = np.tanh(5 * u2[n] * gain / 2)

    fc = 20000 / ratio
    Q = 1 / np.sqrt(2)
    a, b = LPF(fs, fc, Q)
    u4 = filter(a, b, u3)

    for n in range(length_of_x):
        y[n] = u4[(n - 1) * ratio]

    y /= np.max(np.abs(y))
    y *= level

    return y


# s, fs = sf.read("p7_2(input).wav")
s, fs = sf.read("yamada.wav")

gain = 200
level = 0.1
s = distortion(fs, gain, level, s)
sf.write("p7_2(output).wav", s.copy(), fs)
