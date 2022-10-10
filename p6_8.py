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


fs = 44100
f0 = 440

gate = 3
duration = 4

VCO_A = np.array([0, 0])
VCO_D = np.array([0, 0])
VCO_S = np.array([1, 1])
VCO_R = np.array([0, 0])
VCO_gate = np.array([duration, duration])
VCO_duration = np.array([duration, duration])
VCO_offset = np.array([f0 * 3.5, f0])
VCO_depth = np.array([0, 0])

VCA_A = np.array([0.01, 0.01])
VCA_D = np.array([0, 0])
VCA_S = np.array([1, 1])
VCA_R = np.array([0.01, 0.01])
VCA_gate = np.array([gate, gate])
VCA_duration = np.array([duration, duration])
VCA_offset = np.array([0, 0])
VCA_depth = np.array([1, 1])

length_of_s = int(fs * duration)
s = np.zeros(length_of_s)

vco_m = ADSR(fs, VCO_A[0], VCO_D[0], VCO_S[0], VCO_R[0], VCO_gate[0], VCO_duration[0])
for n in range(length_of_s):
    vco_m[n] = VCO_offset[0] + vco_m[n] * VCO_depth[0]

vca_m = ADSR(fs, VCA_A[0], VCA_D[0], VCA_S[0], VCA_R[0], VCA_gate[0], VCA_duration[0])
for n in range(length_of_s):
    vca_m[n] = VCA_offset[0] + vca_m[n] * VCA_depth[0]

vco_c = ADSR(fs, VCO_A[1], VCO_D[1], VCO_S[1], VCO_R[1], VCO_gate[1], VCO_duration[1])
for n in range(length_of_s):
    vco_c[n] = VCO_offset[1] + vco_c[n] * VCO_depth[1]

vca_c = ADSR(fs, VCA_A[1], VCA_D[1], VCA_S[1], VCA_R[1], VCA_gate[1], VCA_duration[1])
for n in range(length_of_s):
    vca_c[n] = VCA_offset[1] + vca_c[n] * VCA_depth[1]

xm = 0
xc = 0
for n in range(length_of_s):
    s[n] = vca_c[n] * np.sin(2 * np.pi * xc + vca_m[n] * np.sin(2 * np.pi * xm))
    delta_m = vco_m[n] / fs
    xm += delta_m
    if xm >= 1:
        xm -= 1

    delta_c = vco_c[n] / fs
    xc += delta_c
    if xc >= 1:
        xc -= 1

length_of_s_master = int(fs * (duration + 2))
s_master = np.zeros(length_of_s_master)

offset = int(fs * 1)
for n in range(length_of_s):
    s_master[offset + n] += s[n]

master_volume = 0.5
s_master /= np.max(np.abs(s_master))
s_master *= master_volume

sf.write("p6_8(output).wav", s_master, fs)
