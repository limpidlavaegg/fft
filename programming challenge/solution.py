import math
import sys
import time

import numpy as np
from math import sin, cos, pi
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# Dictionary corresponding note names to frequencies (Hz). Only need to store one octave.
note_dict = {
    261.626: "C",
    277.183: "C#",
    293.665: "D",
    311.127: "D#",
    329.628: "E",
    349.228: "F",
    369.994: "F#",
    391.995: "G",
    415.305: "G#",
    440.000: "A",
    466.164: "A#",
    493.883: "B",
}

# List of note frequencies.
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

# Defines frequency range a note must fall within before lookup in the list/dict.
min_comp_freq = 255.0
max_comp_freq = 505.0

# Major third and minor third ratios. Useful for some functions.
min_third = pow(2.0, 3.0/12.0)
maj_third = pow(2.0, 4.0/12.0)


# Fast Fourier transform.
def fft(X: list[float]) -> list[float]:
    N = len(X)
    # Base case. Transform of a single element is itself.
    if N == 1:
        return X
    Xodd = []
    Xeven = []
    # Split input into two sub-cases of even and odd indices.
    for i in range(N):
        if i % 2 == 0:
            Xeven.append(X[i])
        else:
            Xodd.append(X[i])
    # Recursively calculate transform of sub-cases.
    Yodd = fft(Xodd)
    Yeven = fft(Xeven)
    Y = [0] * N
    arg = -2*pi/N
    # Merge recursive results to get full transform. Utilizes periodicity of complex exponential to combine results.
    for k in range(N//2):
        root = complex(real=cos(arg*k), imag=sin(arg*k))
        Y[k] = Yeven[k] + root*Yodd[k]
        Y[k+N//2] = Yeven[k] - root*Yodd[k]
    return Y


# Find indices of peaks in FFT output.
def fft_find_peaks(signal):
    peak_indices, _ = find_peaks(signal, height=100)
    return peak_indices


# Given a frequency, find the frequency closest to it in the frequency list. To be used for note name lookup.
def find_closest(freq):
    # Multiplying or dividing frequency by 2 does not change the note name, so we only need to store one octave.
    while freq < min_comp_freq:
        freq *= 2
    while freq > max_comp_freq:
        freq /= 2

    # Find the closest frequency in list and return.
    closest_freq = note_frequencies[0]
    min_dist = abs(note_frequencies[0] - freq)
    for i in range(len(note_frequencies)):
        dist = abs(note_frequencies[i] - freq)
        if dist < min_dist:
            min_dist = dist
            closest_freq = note_frequencies[i]
    return closest_freq


# For the frequencies returned by the FFT, find the closest values in list for lookup in dict.
def get_exact_freqs(frequencies):
    exact_frequencies = []
    for freq in frequencies:
        exact_frequencies.append(find_closest(freq))
    return exact_frequencies


# Given exact frequencies, lookup note names in dict and return.
def get_note_names(frequencies):
    # Should only put exact frequencies into this.
    note_names = []
    for freq in frequencies:
        note_names.append(note_dict[freq])
    return note_names


# Bulk of code for chord determination. Determines if a given chord is in root position. If it is, return the chord
# root and quality, e.g. C maj.
def is_root_pos(frequencies):
    tolerance = 0.03 # need some tolerance in ratios between notes - may need to adjust
    # Calculate the intervals between notes using frequency ratios.
    first_interval = frequencies[1] / frequencies[0]
    second_interval = frequencies[2] / frequencies[1]
    # Boolean values for interval type. Checks if difference between observed and true interval is within tolerance.
    int1_is_min_third = abs(first_interval - min_third) < tolerance
    int2_is_min_third = abs(second_interval - min_third) < tolerance
    int1_is_maj_third = abs(first_interval - maj_third) < tolerance
    int2_is_maj_third = abs(second_interval - maj_third) < tolerance
    # Chord is in root position if both intervals are a type of third.
    is_root_pos = (int1_is_maj_third or int1_is_min_third) and (int2_is_maj_third or int2_is_min_third)
    # Depending on interval types, determine chord quality.
    if is_root_pos:
        if int1_is_maj_third and int2_is_min_third:
            chord_type = "maj"
        elif int1_is_min_third and int2_is_maj_third:
            chord_type = "min"
        elif int1_is_min_third and int2_is_min_third:
            chord_type = "dim"
        else:
            chord_type = "n/a"
        return ["T", chord_type]
    else:
        return ["F", "n/a"]


# Repeatedly move the lowest frequency note up by an octave until chord is in root position, then return root,
# chord type, and frequencies in root position order.
def get_chord_type(frequencies):
    # Want to get chord into root position so that we can determine its quality (maj/min/dim).
    while not is_root_pos(frequencies)[0] == "T":
        # Double lowest frequency, preserves note name and chord quality but changes intervals.
        frequencies[0] *= 2
        # Rearrange notes in frequency order after doubling lowest.
        frequencies.sort()
    # While in root position, the root is the lowest note.
    root_note = note_dict[find_closest(frequencies[0])]
    return root_note, is_root_pos(frequencies)[1], frequencies  # returns frequencies sorted


# Given bass (lowest) note of a chord and the notes in root position, determine the chord inversion.
# Root in bass = root pos (0); third in bass = 1st inv. (1); fifth in bass = 2nd inv. (2)
def get_chord_inversion(bass_note, root_pos_notes):
    for i in range(len(root_pos_notes)):
        if root_pos_notes[i] == bass_note:
            return i
    return -1


# Read in input parameters from first line of input
params = sys.stdin.readline().strip().split(" ")

num_chords = int(params[0])
num_samples = int(params[1])
duration = float(params[2])

for i in range(num_chords):
    # Read waveform from input and convert to list of floats
    input_line = sys.stdin.readline().strip().split(" ")
    waveform = [float(s) for s in input_line]

    # print(waveform)

    # Get FFT of waveform and take absolute value of complex output to get frequency magnitudes.
    fft_result = np.abs(fft(waveform))
    pos_result = fft_result[:len(fft_result)//2]  # Only the first half of the output corresponds to real frequencies

    # Calculate frequency bins to correspond indices of peaks in FFT output to frequencies in Hz.
    freq_bins = np.fft.fftfreq(len(fft_result), duration/num_samples)  # sample interval = duration / num_samples
    freq_bins = freq_bins[:len(freq_bins)//2]

    """
    plt.plot(freq_bins, pos_result)
    plt.show()
    """

    # Get indices of peaks in FFT output, then use to find peak frequencies.
    peak_indices = fft_find_peaks(pos_result)
    peak_frequencies = freq_bins[peak_indices]

    # print(peak_frequencies)

    if len(peak_frequencies) != 3:
        print("Error: more/less than 3 peaks detected")
        exit(1)

    # ----------------------------------------------------
    # Above is fft code, below is chord determination code
    # ----------------------------------------------------

    # Correct to exact frequencies to account for frequency bin variation.
    exact_frequencies = get_exact_freqs(peak_frequencies)

    # print(exact_frequencies)

    # Get note names. Will be in ascending order of frequency.
    notes = get_note_names(exact_frequencies)

    # Get bass note. Will be used to determine inversion.
    bass_note = notes[0]

    # Get chord root and quality.
    root, chord_type, root_pos_freqs = get_chord_type(exact_frequencies)

    # Given notes rearranged into root position and bass note, determine chord inversion.
    root_pos_exact_freqs = get_exact_freqs(root_pos_freqs)
    root_pos_notes = get_note_names(root_pos_exact_freqs)
    inversion = get_chord_inversion(bass_note, root_pos_notes)

    # Print out: notes (in ascending frequency order), root, chord type, inversion
    for note in notes:
        print(note, end=" ")
    print()
    print(root, end=" ")
    print(chord_type, end=" ")
    print(inversion, end=" ")
    print()
