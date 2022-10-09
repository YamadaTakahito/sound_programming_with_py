import numpy as np
import soundfile as sf


def sine_wave(fs, vco, duration):
    length_of_s = int(fs * duration)
    s = np.zeros(length_of_s)
    x = 0

    for n in range(length_of_s):
        s[n] = np.sin(2 * np.pi * x)
        delta = vco[n] / fs
        x += delta
        if x >= 1:
            x -= 1

    return s


def sawtooth_wave(fs, vco, duration):
    length_of_s = int(fs * duration)
    s = np.zeros(length_of_s)
    x = 0
    for n in range(length_of_s):
        s[n] = -2 * x + 1
        delta = vco[n] / fs
        if 0 <= x and x < delta:
            t = x / delta
            d = -t * t + 2 * t - 1
            s[n] += d
        elif 1 - delta < x and x <= 1:
            t = (x - 1) / delta
            d = t * t + 2 * t + 1
            s[n] += d

        x += delta
        if x >= 1:
            x -= 1
    return s


def square_wave(fs, vco, duration):
    length_of_s = int(fs * duration)
    s = np.zeros(length_of_s)
    x = 0
    for n in range(length_of_s):
        if x < 0.5:
            s[n] = 1
        else:
            s[n] = -1

        delta = vco[n] / fs
        if 0 <= x and x < delta:
            t = x / delta
            d = -t * t + 2 * t - 1
            s[n] += d
        elif 1 - delta < x and x <= 1:
            t = (x - 1) / delta
            d = t * t + 2 * t + 1
            s[n] += d

        if 0.5 <= x and x < 0.5 + delta:
            t = (x - 0.5) / delta
            d = -t * t + 2 * t - 1
            s[n] -= d
        elif 0.5 - delta < x and x <= 0.5:
            t = (x - 0.5) / delta
            d = t * t + 2 * t + 1
            s[n] -= d

        x += delta
        if x >= 1:
            x -= 1

    return s


fs = 44100
duration = 1

length_of_s = int(fs * duration)
vco = np.zeros(length_of_s)
vca = np.zeros(length_of_s)

for n in range(length_of_s):
    vco[n] = 440
    vca[n] = 1

# s = sine_wave(fs, vco, duration)
# s = sawtooth_wave(fs, vco, duration)
s = square_wave(fs, vco, duration)

for n in range(length_of_s):
    s[n] *= vca[n]

for n in range(int(fs * 0.01)):
    s[n] *= n / (fs * 0.01)
    s[length_of_s - n - 1] *= n / (fs * 0.01)

length_of_s_master = int(fs * (duration + 2))
s_master = np.zeros(length_of_s_master)

offset = int(fs * 1)
for n in range(length_of_s):
    s_master[offset + n] += s[n]

master_volume = 0.5
s_master /= np.max(np.abs(s_master))
s_master *= master_volume

sf.write("p6_1(output_square).wav", s_master, fs)
