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


s, fs = sf.read("p5_1(input).wav")
print(fs)
length_of_s = len(s)

t = np.zeros(length_of_s)
for n in range(length_of_s):
    t[n] = n / fs

plt.figure()
plt.plot(t, s)
plt.axis([0, 0.008, -1, 1])
plt.xlabel("time [s]")
plt.ylabel("amplitude")
plt.savefig("p5_1a.png")

N = 1024

w = Hanning_window(N)
x = np.zeros(N)
for n in range(N):
    x[n] = s[n] * w[n]

X = np.fft.fft(x, N)
X_abs = np.abs(X)

f = np.zeros(N)
for k in range(N):
    f[k] = fs * k / N

plt.figure()
plt.plot(f[0: int(N / 2)], X_abs[0: int(N / 2)])
plt.axis([0, 4000, 0, 200])

plt.xlabel("frequency [Hz]")
plt.ylabel("amplitude")
plt.savefig("p5_1b.png")

plt.show()
