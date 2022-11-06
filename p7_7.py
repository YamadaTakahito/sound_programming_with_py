import numpy as np
import soundfile as sf


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


fs = 44100
duration = 4

depth = 50
rate = 1

length_of_s = int(fs * duration)
vco = np.zeros(length_of_s)
vca = np.zeros(length_of_s)

for n in range(length_of_s):
    vco[n] = 440 + depth * np.sin(2 * np.pi * rate * n / fs)
    vca[n] = 1

s = sawtooth_wave(fs, vco, duration)

for n in range(length_of_s):
    s[n] *= vca[n]

for n in range(int(fs * 0.01)):
    s[n] *= n / (fs * 0.01)
    s[length_of_s - n - 1] *= n / (fs * 0.01)

length_of_s_master = int(fs * (duration + 2))
s_master = np.zeros(length_of_s_master)

offset = int(fs)
for n in range(length_of_s):
    s_master[offset + n] += s[n]

master_volume = 0.5
s_master /= np.max(np.abs(s_master))
s_master *= master_volume

sf.write("p7_7(output).wav", s_master, fs)
