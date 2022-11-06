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


s0, fs = sf.read("p8_4(output).wav")
length_of_s = len(s0)

s0L = s0[:, 0]
s0R = s0[:, 1]

s1L = np.zeros(length_of_s)
s1R = np.zeros(length_of_s)

for n in range(length_of_s):
    s1L[n] = s0L[n] - s0R[n]
    s1R[n] = s0R[n] - s0L[n]

s2L = np.zeros(length_of_s)
s2R = np.zeros(length_of_s)

N = 4096
shift_size = int(N / 2)
number_of_frame = int((length_of_s - (N - shift_size)) / shift_size)

xL = np.zeros(N)
xR = np.zeros(N)
w = Hanning_window(N)

fmin = round(200 * N / fs)
fmax = round(8000 * N / fs)

for frame in range(number_of_frame):
    offset = shift_size * frame
    for n in range(N):
        xL[n] = s0L[offset + n] * w[n]
        xR[n] = s0R[offset + n] * w[n]

    XL = np.fft.fft(xL, N)
    XL_abs = np.abs(XL)
    XL_angle = np.angle(XL)

    XR = np.fft.fft(xR, N)
    XR_abs = np.abs(XR)
    XR_angle = np.angle(XR)

    for k in range(fmin, fmax):
        if np.abs(XL[k] + XR[k]) != 0:
            num = np.abs(XL[k] - XR[k]) * np.abs(XL[k] - XR[k])
            den = np.abs(XL[k] + XR[k]) * np.abs(XL[k] + XR[k])
            d = num / den
            if d < 0.001:
                XL_abs[k] = 0.000001
                XL_abs[N - k] = XL_abs[k]
                XR_abs[k] = 0.000001
                XR_abs[N - k] = XR_abs[k]

    YL = XL_abs * np.exp(1j * XL_angle)
    yL = np.fft.ifft(YL, N)
    yL = np.real(yL)

    YR = XR_abs * np.exp(1j * XR_angle)
    yR = np.fft.ifft(YR, N)
    yR = np.real(yR)

    for n in range(N):
        s2L[offset + n] += yL[n]
        s2R[offset + n] += yR[n]

for n in range(length_of_s):
    s2L[n] = s1L[n] * 0.2 + s2L[n] * 0.8
    s2R[n] = s1R[n] * 0.2 + s2R[n] * 0.8

s2 = np.zeros((length_of_s, 2))
s2[:, 0] = s2L
s2[:, 1] = s2R

sf.write("p8_6(output).wav", s2, fs)
