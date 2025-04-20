#include <iostream>
#include <vector>
#include <string>
#include <cstdio>
#include <math.h>
#include <iomanip>
#include <bits/stdc++.h>
using namespace std;

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
        complex<double> factor(0, (-2.0 * M_PI * i) / n);
        factor = exp(factor) * odds[i];
        // Front half of the result: evens_i + exp(-2im*pi*i/n) * odds_i
        ret[i] = evens[i] + factor;
        // Back half of the result: evens_i - exp(-2im*pi*i/n) * odds_i
        ret[i + half_n] = evens[i] - factor;
    }
    return ret;
}

int main() {
    int n = -1;
    cin >> n;

    vector<complex<double>> in(n);
    for (int i = 0; i < n; i++) {
        double val = -1.0;
        cin >> val;
        in[i] = complex<double>(val, 0.0);
    }

    vector<complex<double>> out = fft(in);
    for (int i = 0; i < n; i++) {
        cout << fixed << setprecision(5) << "(" << out[i].real() << ", " << out[i].imag() << ")\n";
    }
}