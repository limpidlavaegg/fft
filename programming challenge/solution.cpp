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
vector<pair<double, string>> note_dict = {
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
double min_comp_freq = 255.0;
double max_comp_freq = 505.0;

double min_third = pow(2.0, 3.0/12.0);
double maj_third = pow(2.0, 4.0/12.0);

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

vector<int> fft_find_peaks(vector<double> signal) {
    // TODO - find peaks in signal. Find local maxima with min threshold?
}


int main() {

    int numChords;
    int numSamples;
    double duration;

    // Read in main parameters
    cin >> numChords;
    cin >> numSamples;
    cin >> duration;

    // Main loop
    for (int i = 0; i < numChords; i++) {
        vector<complex<double>> waveform(numSamples);
        double sample;

        // Read samples in, convert to complex numbers, and add to waveform list
        for (int j = 0; j < numSamples; j++) {
            cin >> sample;
            waveform[j] = complex<double>(sample, 0);
        }

        // Compute FFT of waveform
        vector<complex<double>> fftResult = fft(waveform);

        vector<double> realResult = abs(fftResult);
    }

    return 0;
}