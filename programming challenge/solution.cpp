#include <iostream>
#include <vector>
#include <string>
#include <cstdio>
#include <math.h>
#include <cmath>
#include <iomanip>
#include <bits/stdc++.h>

using namespace std;

// Dictionary corresponding note names to frequencies. Only need to store one octave.
vector<pair<double, string>> noteDict = {
    {261.626, "C"},
    {277.183, "C#"},
    {293.665, "D"},
    {311.127, "D#"},
    {329.628, "E"},
    {349.228, "F"},
    {369.994, "F#"},
    {391.995, "G"},
    {415.305, "G#"},
    {440.000, "A"},
    {466.164, "A#"},
    {493.883, "B"}
};

// Defines frequency range a note must fall within before lookup in the list/dict.
double minCompFreq = 255.0;
double maxCompFreq = 505.0;

// Major third and minor third ratios. Useful for some functions.
double minThird = pow(2.0, 3.0/12.0);
double majThird = pow(2.0, 4.0/12.0);

vector<complex<double>> fft(vector<complex<double>> in) {
    int n = in.size();
    // Base case: in contains just one element -> the result of the transform is the element itself
    if (n == 1) {
        return in;
    }

    // Split array into odd and even indices for divide and conquer
    int half_n = n / 2;
    // Init arrays for storing values at the odd and even indices
    vector<complex<double>> odds(half_n);
    vector<complex<double>> evens(half_n);
    // Counters to keep track of the cur index in odds and evens
    int odds_i = 0;
    int evens_i = 0;
    // Split in by iterating over all values, and storing into odds or evens depending on cur index
    for (int i = 0; i < n; i++) {
        if (i % 2 == 0) {
            evens[evens_i] = in[i];
            evens_i++;
        }
        else {
            odds[odds_i] = in[i];
            odds_i++;
        }
    }

    // Recursively calculate the DFT on odds and evens separately
    odds = fft(odds);
    evens = fft(evens);

    // Merge the resultant transforms of odds and evens using trigonometric constant coefficients ("twiddle factors")
    // Init array for saving the results
    vector<complex<double>> ret(n);
    for (int i = 0; i < half_n; i++) {
        // Calc. twiddle factor: exp(-2im*pi*i/n)
        // Here, the complex number that forms the baseline for the factor has no rational component and only an imaginary component
        complex<double> factor(0, (-2.0 * M_PI * i) / n);
        factor = exp(factor);
        // Front half of the result: evens_i + exp(-2im*pi*i/n) * odds_i
        ret[i] = evens[i] + (factor * odds[i]);
        // Back half of the result: evens_i - exp(-2im*pi*i/n) * odds_i
        ret[i + half_n] = evens[i] - (factor * odds[i]);
    }
    return ret;
}

// Find indices of peaks in FFT output.
vector<int> fftFindPeaks(vector<double> signal, int threshold) {
    vector<int> peaks;
    for (int i = 1; i < signal.size() - 1; i++) {
        // Add peak if is local maxima (higher than neighbors) and greater than threshold value.
        if (signal[i] > signal[i - 1] && signal[i] > signal[i + 1] && signal[i] > threshold) {
            peaks.push_back(i);
        }
    }
    return peaks;
}

// Calculate the corresponding frequency bins for indices of FFT output.
vector<double> getFreqBins(int numSamples, double sampleInterval) {
    vector<double> freqBins(numSamples);
    for (int i = 0; i < numSamples; i++) {
        freqBins[i] = i / (numSamples * sampleInterval);
    }
    return freqBins;
}

// Given a frequency, find the frequency closest to it in the frequency list. To be used for note name lookup.
double findClosest(double freq) {
    // Multiplying or dividing frequency by 2 does not change the note name, so we only need to store one octave.
    while (freq < minCompFreq) {
        freq *= 2;
    }
    while (freq > maxCompFreq) {
        freq /= 2;
    }
    // Find the closest frequency in list and return.
    double closestFreq = noteDict[0].first;
    double minDist = abs(noteDict[0].first - freq);
    for (int i = 0; i < noteDict.size(); i++) {
        double dist = abs(noteDict[i].first - freq);
        if (dist < minDist) {
            minDist = dist;
            closestFreq = noteDict[i].first;
        }
    }
    return closestFreq;
}

// For the frequencies returned by the FFT, find the closest values in list for lookup in dict.
vector<double> getExactFreqs(vector<double> frequencies) {
    vector<double> exactFrequencies = {};
    for (double freq : frequencies) {
        exactFrequencies.push_back(findClosest(freq));
    }
    return exactFrequencies;
}

// Given exact frequencies, lookup note names in dict and return.
vector<string> getNoteNames(vector<double> frequencies) {
    vector<string> noteNames = {};
    for (double freq : frequencies) {
        for (int i = 0; i < noteDict.size(); i++) {
            if (noteDict[i].first == freq) {
                noteNames.push_back(noteDict[i].second);
                break;
            }
        }
    }
    return noteNames;
}

// Bulk of code for chord determination. Determines if a given chord is in root position. If it is, return the chord
// root and quality, e.g. C maj.
pair<string, string> isRootPos(vector<double> frequencies) {
    double tolerance = 0.03;
    // Calculate the intervals between notes using frequency ratios.
    double firstInterval = frequencies[1] / frequencies[0];
    double secondInterval = frequencies[2] / frequencies[1];
    // Boolean values for interval type. Checks if difference between observed and true interval is within tolerance.
    bool int1IsMinThird = abs(firstInterval - minThird) < tolerance;
    bool int2IsMinThird = abs(secondInterval - minThird) < tolerance;
    bool int1IsMajThird = abs(firstInterval - majThird) < tolerance;
    bool int2IsMajThird = abs(secondInterval - majThird) < tolerance;
    // Chord is in root position if both intervals are a type of third.
    bool isRootPos = (int1IsMajThird or int1IsMinThird) and (int2IsMajThird or int2IsMinThird);
    if (isRootPos) {
        if (int1IsMajThird && int2IsMinThird) {
            return {"T", "maj"};
        }
        if (int1IsMinThird && int2IsMajThird) {
            return {"T", "min"};
        }
        if (int1IsMinThird && int2IsMinThird) {
            return {"T", "dim"};
        }
    }
    return {"F", "n/a"};
}

// Repeatedly move the lowest frequency note up by an octave until chord is in root position, then return root,
// chord type, and frequencies in root position order.
pair<pair<string, string>, vector<double>> getChordType(vector<double> frequencies) {
    // Want to get chord into root position so that we can determine its quality (maj/min/dim).
    while (isRootPos(frequencies).first != "T") {
        // Double lowest frequency, preserves note name and chord quality but changes intervals.
        frequencies[0] *= 2;
        // Rearrange notes in frequency order after doubling lowest.
        sort(frequencies.begin(), frequencies.end());
    }
    // While in root position, the root is the lowest note.
    double rootFreq = findClosest(frequencies[0]);
    string rootNote;
    for (int i = 0; i < noteDict.size(); i++) {
        if (noteDict[i].first == rootFreq) {
            rootNote = noteDict[i].second;
            break;
        }
    }
    return {{rootNote, isRootPos(frequencies).second}, frequencies};
}

// Given bass (lowest) note of a chord and the notes in root position, determine the chord inversion.
// Root in bass = root pos (0); third in bass = 1st inv. (1); fifth in bass = 2nd inv. (2)
int getChordInversion(string bassNote, vector<string> rootPosNotes) {
    for (int i = 0; i < rootPosNotes.size(); i++) {
        if (rootPosNotes[i] == bassNote) {
            return i;
        }
    }
    return -1;
}


int main() {

    int numChords;
    int numSamples;
    double duration;

    // Read in main parameters.
    cin >> numChords;
    cin >> numSamples;
    cin >> duration;

    // Main loop.
    for (int i = 0; i < numChords; i++) {
        vector<complex<double>> waveform(numSamples);
        double sample;

        // Read samples in, convert to complex numbers, and add to waveform list.
        for (int j = 0; j < numSamples; j++) {
            cin >> sample;
            waveform[j] = complex<double>(sample, 0);
        }

        // Compute FFT of waveform.
        vector<complex<double>> fftResult = fft(waveform);

        // Get magnitude of complex results.
        vector<double> realResult;
        for(complex<double> z : fftResult) {
            realResult.push_back(abs(z));
        }

        // Only first half of output represents real frequencies.
        int mid = realResult.size() / 2;

        // Get corresponding frequency bins.
        vector<double> posResult(realResult.begin(), realResult.begin() + mid);
        vector<double> freqBins = getFreqBins(numSamples, duration/numSamples);
        vector<double> posFreqBins(freqBins.begin(),freqBins.begin() + mid);

        // Find peaks in FFT output.
        vector<int> peakIndices = fftFindPeaks(posResult, 100);
        vector<double> peakFrequencies;
        for (int k = 0; k < peakIndices.size(); k++) {
            peakFrequencies.push_back(posFreqBins[peakIndices[k]]);
        }

        // ----------------------------------------------------
        // Above is fft code, below is chord determination code
        // ----------------------------------------------------

        // Correct to exact frequencies to account for frequency bin variation.
        vector<double> exactFrequencies = getExactFreqs(peakFrequencies);
        // Get note names. Will be in ascending order of frequency.
        vector<string> notes = getNoteNames(exactFrequencies);

        // Get chord root and quality.
        pair<pair<string, string>, vector<double>> chordTypeRet = getChordType(exactFrequencies);
        string rootNote = chordTypeRet.first.first;
        string chordType = chordTypeRet.first.second;

        // Get notes rearranged into root position, then determine chord inversion.
        vector<double> rootPosExactFreqs = getExactFreqs(chordTypeRet.second);
        vector<string> rootPosNotes = getNoteNames(rootPosExactFreqs);
        // Use base note and root position notes.
        int inversion = getChordInversion(notes[0], rootPosNotes);

        // Print results.
        for (string note : notes) {
            printf("%s ", note.c_str());
        }
        printf("\n%s %s %d\n", rootNote.c_str(), chordType.c_str(), inversion);

    }

    return 0;
}