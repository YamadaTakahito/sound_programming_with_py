import numpy as np
import soundfile as sf


def sine_wave(fs, f, a, duration):
    length_of_s = int(fs * duration)
    s = np.zeros(length_of_s)
    for n in range(length_of_s):
        s[n] = np.sin(2 * np.pi * f * n / fs)

    for n in range(int(fs * 0.01)):
        s[n] *= n / (fs * 0.01)
        s[length_of_s - n - 1] *= n / (fs * 0.01)

    gain = a / np.max(np.abs(s))
    s *= gain
    return s


score = np.array([[1, 2, 659.26, 0.5, 1],
                  [1, 3, 587.33, 0.5, 1],
                  [1, 4, 523.25, 0.5, 1],
                  [1, 5, 493.88, 0.5, 1],
                  [1, 6, 440.00, 0.5, 1],
                  [1, 7, 392.00, 0.5, 1],
                  [1, 8, 440.00, 0.5, 1],
                  [1, 9, 493.88, 0.5, 1],
                  [2, 2, 261.63, 0.5, 1],
                  [2, 3, 196.00, 0.5, 1],
                  [2, 4, 220.00, 0.5, 1],
                  [2, 5, 164.81, 0.5, 1],
                  [2, 6, 174.61, 0.5, 1],
                  [2, 7, 130.81, 0.5, 1],
                  [2, 8, 174.61, 0.5, 1],
                  [2, 9, 196.00, 0.5, 1]])

tempo = 120
number_of_track = 2
end_of_track = (4 + 16) * (60 / tempo)
number_of_note = score.shape[0]

fs = 44100
length_of_s_master = int(fs * (end_of_track + 2))
track = np.zeros((length_of_s_master, number_of_track))
s_master = np.zeros(length_of_s_master)

for i in range(number_of_note):
    j = int(score[i, 0] - 1)
    onset = score[i, 1]
    f = score[i, 2]
    a = score[i, 3]
    duration = score[i, 4]

    s = sine_wave(fs, f, a, duration)
    length_of_s = len(s)
    offset = int(fs * onset)
    for n in range(length_of_s):
        track[offset + n, j] += s[n]

for j in range(number_of_track):
    for n in range(length_of_s_master):
        s_master[n] += track[n, j]

master_volume = 0.5
s_master /= np.max(np.abs(s_master))
s_master *= master_volume

sf.write("p3_1.wav", s_master, fs)
