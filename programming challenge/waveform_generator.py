import math
import numpy as np
import matplotlib.pyplot as plt


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


# list of frequencies in Hz of sine waves to add together and sample
# For example, [60, 90] would generate the sum of sin(2pi * 60 * t) and sin(2pi * 90 * t), 60Hz and 90Hz waves
my_frequencies = [100, 125, 150]

# Number of evenly spaced samples to take of the composite waveform over the chosen time interval
# For example, 100 samples over a 10-second interval would result in 10 samples per second
# This number should be quite high to get appropriate waveform resolution
# It should also be higher the greater the frequency or complexity of the waveform
my_num_samples = 1024

# Duration to sample the waveform
# For high frequency waveforms, this can be quite short
# for very low frequency waveforms, may want to sample a longer duration to capture periodicity
my_duration = 0.2

# Get resultant samples of waveform from above parameters
my_result = waveform_generator(my_frequencies, my_num_samples, my_duration)
print(my_result)

# Plot results
plt.plot(np.arange(0, my_duration, my_duration / my_num_samples), my_result)
plt.show()
