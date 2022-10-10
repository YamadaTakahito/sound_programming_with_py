import numpy as np
import soundfile as sf


def ADSR(fs, A, D, S, R, gate, duration):
    A = int(fs * A)
    D = int(fs * D)
    R = int(fs * R)
    gate = int(fs * gate)
    duration = int(fs * duration)
    e = np.zeros(duration)

    if A != 0:
        for n in range(A):
            e[n] = (1 - np.exp(-5 * n / A)) / (1 - np.exp(-5))
    if D != 0:
        for n in range(A, gate):
            e[n] = 1 + (S - 1) * (1 - np.exp(-5 * (n - A) / D))
    else:
        for n in range(A, gate):
            e[n] = S
    if R != 0:
        for n in range(gate, duration):
            e[n] = e[gate - 1] - e[gate - 1] * (1 - np.exp(-5 * (n - gate + 1) / R))
    return e


def LPF(fs, fc, Q):
    fc /= fs
    fc = np.tan(np.pi * fc) / (2 * np.pi)
    a = np.zeros(3)
    b = np.zeros(3)
    a[0] = 1 + 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc
    a[1] = (8 * np.pi * np.pi * fc * fc - 2) / a[0]
    a[2] = (1 - 2 * np.pi * fc / Q + 4 * np.pi * np.pi * fc * fc) / a[0]
    b[0] = 4 * np.pi * np.pi * fc * fc / a[0]
    b[1] = 8 * np.pi * np.pi * fc * fc / a[0]
    b[2] = 4 * np.pi * np.pi * fc * fc / a[0]
    a[0] = 1
    return a, b


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
f0 = 440

gate = 3
duration = 4

VCO_A = np.array([0])
VCO_D = np.array([0])
VCO_S = np.array([1])
VCO_R = np.array([0])
VCO_gate = np.array([duration])
VCO_duration = np.array([duration])
VCO_offset = np.array([f0])
VCO_depth = np.array([0])

VCF_A = np.array([0])
VCF_D = np.array([0])
VCF_S = np.array([1])
VCF_R = np.array([0])
VCF_gate = np.array([duration])
VCF_duration = np.array([duration])
VCF_offset = np.array([f0 * 2])
VCF_depth = np.array([0])

VCA_A = np.array([0.01])
VCA_D = np.array([0])
VCA_S = np.array([1])
VCA_R = np.array([0.01])
VCA_gate = np.array([gate])
VCA_duration = np.array([duration])
VCA_offset = np.array([0])
VCA_depth = np.array([1])

length_of_s = int(fs * duration)
s0 = np.zeros(length_of_s)
s1 = np.zeros(length_of_s)

vco = ADSR(fs, VCO_A[0], VCO_D[0], VCO_S[0], VCO_R[0], VCO_gate[0], VCO_duration[0])
for n in range(length_of_s):
    vco[n] = VCO_offset[0] + vco[n] * VCO_depth[0]

s0 = sawtooth_wave(fs, vco, duration)

vcf = ADSR(fs, VCF_A[0], VCF_D[0], VCF_S[0], VCF_R[0], VCF_gate[0], VCF_duration[0])
for n in range(length_of_s):
    vcf[n] = VCF_offset[0] + vcf[n] * VCF_depth[0]
    if vcf[n] > fs / 2:
        vcf[n] = fs / 2  # 遮断周波数はfs/2とする

Q = 1 / np.sqrt(2)
for n in range(length_of_s):
    a, b = LPF(fs, vcf[n], Q)
    for m in range(0, 3):
        if n - m >= 0:
            s1[n] += b[m] * s0[n - m]

    for m in range(1, 3):
        if n - m >= 0:
            s1[n] += -a[m] * s1[n - m]

vca = ADSR(fs, VCA_A[0], VCA_D[0], VCA_S[0], VCA_R[0], VCA_gate[0], VCA_duration[0])
for n in range(length_of_s):
    vca[n] = VCA_offset[0] + vca[n] * VCA_depth[0]

for n in range(length_of_s):
    s1[n] *= vca[n]

length_of_s_master = int(fs * (duration + 2))
s_master = np.zeros(length_of_s_master)

offset = int(fs * 1)
for n in range(length_of_s):
    s_master[offset + n] += s1[n]

master_volume = 0.5
s_master /= np.max(np.abs(s_master))
s_master *= master_volume

sf.write("p6_7(output).wav", s_master, fs)
