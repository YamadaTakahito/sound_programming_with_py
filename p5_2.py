import numpy as np
import soundfile as sf
from matplotlib import pyplot as plt


def Hanning_window(N):
    w = np.zeros(N)
    if N % 2 == 0:
        for n in range(N):
            w[n] = 0.5 - 0.5 * np.cos(2 * np.pi * n / N)
    else:
        for n in range(N):
            w[n] = 0.5 - 0.5 * np.cos(2 * np.pi * (n + 0.5) / N)
    return w


s, fs = sf.read("p5_2(input).wav")
length_of_s = len(s)

N = 512
shift_size = 64
number_of_frame = int((length_of_s - (N - shift_size)) / shift_size)

x = np.zeros(N)
w = Hanning_window(N)
S = np.zeros((int(N / 2 + 1), number_of_frame))

for frame in range(number_of_frame):
    offset = shift_size * frame

    for n in range(N):
        x[n] = s[offset + n] * w[n]

    X = np.fft.fft(x, N)
    X_abs = np.abs(X)

    for k in range(int(N / 2 + 1)):
        S[k, frame] = 20 * np.log10(X_abs[k])

plt.figure()
xmin = (N / 2) / fs
xmax = (shift_size * (number_of_frame - 1) + N / 2) / fs
ymin = 0
ymax = fs / 2
plt.imshow(S, aspect='auto', cmap='Greys', origin="lower", vmin=0, vmax=20, extent=[xmin, xmax, ymin, ymax])
plt.axis([0, length_of_s / fs, 0, fs / 2])
plt.xlabel("time [s]")
plt.ylabel("frequency [Hz]")
plt.savefig("p5_2.png")

plt.show()
