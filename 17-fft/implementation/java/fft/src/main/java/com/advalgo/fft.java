package com.advalgo;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import org.apache.commons.math3.complex.*;

public class fft {

    public static Complex[] fft(Complex[] in) {
        // NOTE: in must be an even length
        int n = in.length;
        // Base case: in contains just one element -> the result of the transform is the element itself
        if (n == 1) {
            return in;
        }

        // Split array into odd and even indices to calculate a DFT via divide-and-conquer
        int half_n = n / 2;
        // Init arrays for storing values at the odd and even indices
        Complex[] odds = new Complex[half_n];
        Complex[] evens = new Complex[half_n];
        // Counters to keep track of the cur index in odds and evens
        int odds_i = 0;
        int evens_i = 0;
        // Split the input data by iterating over all values, and storing into odds or evens depending on cur index
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

        // Recursively calculate the DFT on odds and evens separately, we will merge the results below
        odds = fft(odds);
        evens = fft(evens);

        // Merge the resultant transforms of odds and evens using trigonometric constant coefficients ("twiddle factors")
        // Init array for saving the results
        Complex[] ret = new Complex[n];
        for (int i = 0; i < half_n; i++) {
            // Calc. twiddle factor: exp(-2im*pi*i/n)
            // Here, the complex number that forms the baseline for the factor has no rational component and only an imaginary component
            Complex factor = new Complex(0, (-2.0 * Math.PI * i) / n);
            factor = factor.exp().multiply(odds[i]);
            // Front half of the result: evens_i + exp(-2im*pi*i/n) * odds_i
            ret[i] = evens[i].add(factor);
            // Back half of the result: evens_i - exp(-2im*pi*i/n) * odds_i
            ret[i + half_n] = evens[i].subtract(factor);
        }
        return ret;
    }

    public static void main(String[] args) throws IOException {
        // Set up to read input from command line
        BufferedReader r = new BufferedReader(new InputStreamReader(System.in));

        // Number of input values to expect
        int n = Integer.parseInt(r.readLine());

        // Init each input value as a complex number and save to an input vector
        Complex[] in = new Complex[n];
        for (int i = 0; i < n; i++) {
            in[i] = new Complex(Double.parseDouble(r.readLine()));
        }

        // Calculate the FFT and print the results
        Complex[] res = fft(in);
        for (int i = 0; i < n; i++) {
            // System.out.println(res[i].toString());
            System.out.printf("(%.5f, %.5f)\n", res[i].getReal(), res[i].getImaginary());
        }
    }
}

