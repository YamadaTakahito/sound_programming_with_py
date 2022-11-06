import numpy as np
import soundfile as sf


def compressor(threshold, width, ratio, x):
    length_of_x = len(x)
    y = np.zeros(length_of_x)
    gain = 1 / (threshold + (1 - threshold) / ratio)

    for n in range(length_of_x):
        if x[n] < 0:
            sign_of_x = -1
        else:
            sign_of_x = 1

        abs_of_x = np.abs(x[n])

        if abs_of_x < threshold - width / 2:
            abs_of_x = abs_of_x
        elif abs_of_x >= threshold - width / 2 and abs_of_x < threshold + width / 2:
            abs_of_x = abs_of_x + (1 / ratio - 1) * (abs_of_x - threshold + width / 2) * (
                    abs_of_x - threshold + width / 2) / (width * 2)
        elif abs_of_x >= threshold + width / 2:
            abs_of_x = threshold + (abs_of_x - threshold) / ratio

        y[n] = sign_of_x * abs_of_x * gain

    return y


# s, fs = sf.read("p7_3(input).wav")
s, fs = sf.read("yamada.wav")

threshold = 0.2
width = 0.1
ration = 8
s = compressor(threshold, width, ration, s)
sf.write("p7_3(output).wav", s.copy(), fs)
