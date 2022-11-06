import numpy as np
import soundfile as sf


def Hanning_window(N):
    w = np.zeros(N)
    if N % 2 == 0:
        for n in range(N):
            w[n] = 0.5 - 0.5 * np.cos(2 * np.pi * n / N)
    else:
        for n in range(N):
            w[n] = 0.5 - 0.5 * np.cos(2 * np.pi * (n + 0.5) / N)
    return w


s0, fs = sf.read("p7_5(input).wav")
f = np.array(
    [0, 4, 7, 12, 16, 20, 25, 30, 35, 41, 47, 53, 60, 67, 74, 82, 90, 99, 108, 118, 128, 139, 150, 162, 175, 188, 202,
     217, 233, 250, 267, 286, 306, 326, 348, 371, 396, 421, 449, 477, 508, 540, 574, 609, 647, 687, 729, 773, 820, 869,
     922, 977, 1035, 1097, 1161, 1230, 1302, 1379, 1460, 1545, 1635, 1730, 1830, 1936, 2048])
a = np.array(
    [2.113102, 7.881102, 11.075727, 8.863704, 4.013235, 0.932089, 1.197000, 1.457407, 1.107974, 0.403404, 0.357882,
     0.831457, 0.998504, 0.977239, 0.803210, 0.446178, 0.149860, 0.585399, 0.968549, 1.216626, 1.355936, 1.389370,
     1.275824, 0.925896, 0.300999, 0.590605, 1.593167, 2.624420, 3.691557, 4.830407, 6.157985, 7.791523, 9.669384,
     11.712244, 13.612665, 14.868957, 15.269036, 15.070204, 14.665470, 14.323831, 14.172306, 14.265161, 14.594980,
     15.102259, 15.596862, 15.656709, 14.803574, 12.975877, 10.714214, 8.580678, 6.829857, 5.485252, 4.450106, 3.657807,
     3.042211, 2.555303, 2.168048, 1.856382, 1.607098, 1.407719, 1.250445, 1.131747, 1.050209, 1.007424])
N = 4096

number_of_band = 64

H = np.zeros(N)
for band in range(number_of_band):
    fL = f[band]
    fH = f[band + 1]
    for k in range(fL, fH):
        H[k] = a[band]

for k in range(1, int(N / 2)):
    H[N - k] = H[k]

h = np.real(np.fft.ifft(H, N))

for m in range(int(N / 2)):
    tmp = h[m]
    h[m] = h[int(N / 2) + m]
    h[int(N / 2) + m] = tmp

J = 128

b = np.zeros(J + 1)
w = Hanning_window(J + 1)
offset = int(N / 2) - int(J / 2)
for m in range(J + 1):
    b[m] = h[offset + m] * w[m]

length_of_s = len(s0)
s1 = np.zeros(length_of_s)
for n in range(length_of_s):
    for m in range(J + 1):
        if n - m >= 0:
            s1[n] += b[m] * s0[n - m]

master_volume = 1
s1 /= np.max(np.abs(s1))
s1 *= master_volume

sf.write("p7_5(output).wav", s1.copy(), fs)
