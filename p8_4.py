import numpy as np
import soundfile as sf

s0, fs = sf.read("p8_4(output).wav")
length_of_s = len(s0)

s0L = s0[:, 0]
s0R = s0[:, 1]

s1 = np.zeros(length_of_s)

for n in range(length_of_s):
    s1[n] = s0L[n] - s0R[n]

sf.write("p8_5(output).wav", s1, fs)
