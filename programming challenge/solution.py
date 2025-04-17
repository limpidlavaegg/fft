import math
import numpy as np


def fft(waveform):
    # TODO implement this
    return np.zeros(len(waveform))


def find_peaks(fft_result):
    # TODO implement this
    return [10,20,30]


def get_note_names(frequencies):
    # TODO implement this
    return ["C", "E", "G"]


def get_chord_type(notes, frequencies):
    #TODO implement this
    return "C", "maj"


def get_chord_inversion(notes, root):
    #TODO implement this
    return "1"



# TODO read in waveforms, turn into loop to handle multiple
waveform = [1,0,-1,0,1,0]

fft_result = fft(waveform)
frequencies = find_peaks(fft_result)
notes = get_note_names(frequencies)
root, chord_type = get_chord_type(notes, frequencies)
inversion = get_chord_inversion(notes, root)

# TODO print results