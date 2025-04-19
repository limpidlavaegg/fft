package com.advalgo;

import org.apache.commons.math3.complex.*;

public class fft {

    public static Complex[] fft(Complex[] in) {
        // NOTE: in must be an even length
        int n = in.length;
        // Base case: in contains just one element
        if (n == 1) {
            return in;
        }

        // Split array into odd and even indices for divide and conquer
        int half_n = n / 2;
        Complex[] odds = new Complex[half_n];
        int odds_i = 0;
        Complex[] evens = new Complex[half_n];
        int evens_i = 0;
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

        // Recursively calculate the DFT
        odds = fft(odds);
        evens = fft(evens);

        // Start calc. twiddle factor w/ constant -2im*pi
        Complex factor = new Complex(-2.0);
        factor = factor.multiply(Math.PI);
        // Array for saving the results
        Complex[] ret = new Complex[n];
        for (int i = 0; i < half_n; i++) {
            // Finish calc. twiddle factor: exp(-2im*pi*i/n)
            factor = factor.multiply(i).divide(n).exp();
            // Front half of the result
            ret[i] = factor.multiply(evens[i]).add(odds[i]);
            // Back half of the result
            ret[i + half_n] = factor.multiply(evens[i]).subtract(odds[i]);
        }
        return ret;
    }

    public static void main(String[] args) {
        Complex[] in = new Complex[8];
        for (int i = 0; i < 8; i++) {
            if (i % 2 == 0) {
                in[i] = new Complex(1);
            }
            else {
                in[i] = new Complex(-1);
            }
        }

        Complex[] res = fft(in);
        for (int i = 0; i < 8; i++) {
            System.out.println(res[i].toString());
        }
    }
}

