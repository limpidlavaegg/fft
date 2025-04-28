import math
import numpy as np
import matplotlib.pyplot as plt
import random


# Given a list of frequencies, generate a composite waveform of the sum of the given frequencies
# Returns discrete samples of the waveform
def waveform_generator(frequencies, num_samples, duration):
    result = []
    time_step = duration / num_samples
    for i in range(num_samples):
        t = i * time_step
        amplitude = 0
        for j in range(len(frequencies)):
            amplitude += math.sin(2 * math.pi * frequencies[j] * t)
        result.append(amplitude)
    return result


note_frequencies = [
    261.626,
    277.183,
    293.665,
    311.127,
    329.628,
    349.228,
    369.994,
    391.995,
    415.305,
    440.000,
    466.164,
    493.883
]

min_third = pow(2.0, 3.0/12.0)
maj_third = pow(2.0, 4.0/12.0)
perf_fourth = pow(2.0, 5.0/12.0)


# Note to self: need to choose duration and number of samples VERY carefully
# Need enough duration to capture full waveform shape (periodicity)
# Need enough samples for high resolution capture of waveform

waveform_list = []

# lists of frequencies in Hz of sine waves to add together and sample
# For example, [60, 90] would generate the sum of sin(2pi * 60 * t) and sin(2pi * 90 * t), 60Hz and 90Hz waves

# waveform_list.append([1108.731, 1661.219, 2793.826])

num_waveforms = 50
for i in range(num_waveforms):
    root = note_frequencies[random.randint(0, 11)] # get random root
    chord_type = random.randint(0, 2)
    if chord_type == 0:
        first_third = maj_third
        second_third = min_third
    elif chord_type == 1:
        first_third = min_third
        second_third = maj_third
    else:
        first_third = min_third
        second_third = min_third
    """
    lo_hi = random.randint(0, 1)
    if lo_hi == 0:
        root = root * 4
    else:
        root = root / 4
    """
    waveform_list.append([root, root * perf_fourth, root * perf_fourth * first_third])
    waveform_list.append([root, root * second_third, root * perf_fourth * second_third])


# Number of evenly spaced samples to take of the composite waveform over the chosen time interval
# For example, 100 samples over a 10-second interval would result in 10 samples per second
# This number should be quite high to get appropriate waveform resolution
# It should also be higher the greater the frequency or complexity of the waveform
my_num_samples = 4096

# Duration to sample the waveform
# For high frequency waveforms, this can be quite short
# for very low frequency waveforms, may want to sample a longer duration to capture periodicity
my_duration = 0.5

# Get resultant samples of waveform from above parameters

result_list = []
for freqs in waveform_list:
    result_list.append(waveform_generator(freqs, my_num_samples, my_duration))

with open('testcases/test.in.14', 'w') as f:
    f.write(f"{len(result_list)} {my_num_samples} {my_duration:.1f}\n")
    for result in result_list:
        for sample in result:
            f.write(f"{sample:.4f} ")
        f.write("\n")

"""
# Plot results
plt.plot(np.arange(0, my_duration, my_duration / my_num_samples), my_result)
plt.show()
"""
