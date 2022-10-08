import numpy as np
import soundfile as sf

fs = 441000
duration = 1

length_of_s = int(fs * duration)
s = np.zeros(length_of_s)

for n in range(length_of_s):
    s[n] = 0.5 * np.sin(2 * np.pi * 1000 * n / fs)

for n in range(int(fs * 0.01)):
    s[n] *= n / (fs * 0.01)
    s[length_of_s - n - 1] *= n / (fs * 0.01)

length_of_s_master = int(fs * (duration + 2))
s_master = np.zeros(length_of_s_master)

offset = int(fs * 1)
for n in range(length_of_s):
    s_master[offset + n] += s[n]

sf.write("p2_1.wav", s_master, fs)
