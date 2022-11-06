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

length_of_s = int(fs * duration)
vco0 = np.zeros(length_of_s)
vca0 = np.zeros(length_of_s)
vco1 = np.zeros(length_of_s)
vca1 = np.zeros(length_of_s)

for n in range(length_of_s):
    vco0[n] = 440
    vca0[n] = 1
    vco1[n] = 440.5
    vca1[n] = 1

s0 = sawtooth_wave(fs, vco0, duration)
s1 = sawtooth_wave(fs, vco1, duration)

for n in range(length_of_s):
    s0[n] += vca0[n]
    s1[n] += vca1[n]

s2 = s0 + s1

for n in range(int(fs * 0.01)):
    s2[n] *= n / (fs * 0.01)
    s2[length_of_s - n - 1] *= n / (fs * 0.01)

length_of_s_master = int(fs * (duration + 2))
s_master = np.zeros(length_of_s_master)

offset = int(fs * 1)
for n in range(length_of_s):
    s_master[offset + n] += s2[n]

master_volume = 0.5
s_master /= np.max(np.abs(s_master))
s_master *= master_volume

sf.write("p7_8(output).wav", s_master, fs)
