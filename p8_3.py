import numpy as np
import soundfile as sf

number_of_track = 2

fs = 44100
length_of_s_master = int(fs * 12)
track = np.zeros((length_of_s_master, number_of_track))
s_master = np.zeros((length_of_s_master, 2))

s, fs = sf.read("p8_1(output).wav")
track[:, 0] = s
s, fs = sf.read("p8_2(output).wav")
track[:, 1] = s

v = np.array([1, 1])
p = np.array([0.05, 0.05])

for i in range(number_of_track):
    s_master[:, 0] += track[:, i] * v[i] * np.cos(np.pi * p[i] / 2)
    s_master[:, 1] += track[:, i] * v[i] * np.sin(np.pi * p[i] / 2)

master_volume = 0.5
s_master /= np.max(np.abs(s_master))
s_master *= master_volume

sf.write("p8_3(output).wav", s_master.copy(), fs)
