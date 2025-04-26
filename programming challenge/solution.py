import math
import numpy as np

note_dict = {
    261.626 : "C",
    277.183 : "C#",
    293.665 : "D",
    311.127 : "D#",
    329.628 : "E",
    349.228 : "F",
    369.994 : "F#",
    391.995 : "G",
    415.305 : "G#",
    440.000 : "A",
    466.164 : "A#",
    493.883 : "B",
}

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

min_comp_freq = 255.0
max_comp_freq = 505.0

min_third = pow(2.0, 3.0/12.0)
maj_third = pow(2.0, 4.0/12.0)


def fft(waveform):
    # TODO implement this
    return np.zeros(len(waveform))


def find_peaks(fft_result):
    # TODO implement this
    # Should return peaks in ascending order
    return [100,125,150]


def find_closest(freq):
    while freq < min_comp_freq:
        freq *= 2
    while freq > max_comp_freq:
        freq /= 2
    closest_freq = note_frequencies[0]
    min_dist = abs(note_frequencies[0] - freq)
    for i in range(len(note_frequencies)):
        dist = abs(note_frequencies[i] - freq)
        if dist < min_dist:
            min_dist = dist
            closest_freq = note_frequencies[i]
    return closest_freq


def get_exact_freqs(frequencies):
    exact_frequencies = []
    for freq in frequencies:
        exact_frequencies.append(find_closest(freq))
    return exact_frequencies


def get_note_names(frequencies):
    # Should only put exact frequencies into this
    note_names = []
    for freq in frequencies:
        note_names.append(note_dict[freq])
    return note_names

def is_root_pos(frequencies):
    tolerance = 0.03 # might need some tolerance in ratios between notes - may need to adjust
    first_interval = frequencies[1] / frequencies[0]
    second_interval = frequencies[2] / frequencies[1]
    int1_is_min_third = abs(first_interval - min_third) < tolerance
    int2_is_min_third = abs(second_interval - min_third) < tolerance
    int1_is_maj_third = abs(first_interval - maj_third) < tolerance
    int2_is_maj_third = abs(second_interval - maj_third) < tolerance
    is_root_pos = (int1_is_maj_third or int1_is_min_third) and (int2_is_maj_third or int2_is_min_third)
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


def get_chord_type(frequencies):
    #TODO implement this
    #TODO ensure this handles enharmonic equivalents
    while not is_root_pos(frequencies)[0] == "T":
        frequencies[0] *= 2
        frequencies.sort() # Make sure this is correct order
    root_note = note_dict[find_closest(frequencies[0])]
    return root_note, is_root_pos(frequencies)[1], frequencies # returns frequencies sorted


def get_chord_inversion(root_pos_notes, bass_note):
    # TODO make this work!
    for i in range(len(root_pos_notes)):
        if root_pos_notes[i] == bass_note:
            return i
    return -1



# TODO read in waveforms, turn into loop to handle multiple
#waveform = [1,0,-1,0,1,0]
#fft_result = fft(waveform)
#frequencies = find_peaks(fft_result)

# Above is fft code, below is chord determination code

frequencies = [440, 440*min_third, 440*min_third, 440*maj_third] # Should be detected as ACE A min 0
exact_frequencies = get_exact_freqs(frequencies)

notes = get_note_names(exact_frequencies) # only used to print out in ascending freq order
bass_note = notes[0]

root, chord_type, root_pos_freqs = get_chord_type(exact_frequencies)
root_pos_exact_freqs = get_exact_freqs(root_pos_freqs)
root_pos_notes = get_note_names(root_pos_exact_freqs)
inversion = get_chord_inversion(bass_note, root)

# Print out: notes, root, chord type, inversion

# TODO print results