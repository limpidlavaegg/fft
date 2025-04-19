package com.advalgo;

import org.apache.commons.math3.complex.*;

public class fft {
/*
function cooley_tukey(x)
    N = length(x)

    if (N > 2)
        x_odd = cooley_tukey(x[1:2:N])
        x_even = cooley_tukey(x[2:2:N])
    else
        x_odd = x[1]
        x_even = x[2]
    end
    n = 0:N-1
    half = div(N,2)
    factor = exp.(-2im*pi*n/N)
    return vcat(x_odd .+ x_even .* factor[1:half],
                x_odd .- x_even .* factor[1:half])

end

*/

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
                System.out.println(evens_i);
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
            if (i < half_n) {
                // Front half of the result
                ret[i] = factor.multiply(evens[i]).add(odds[i]);
            }
            else {
                // Back half of the result
                ret[i] = factor.multiply(evens[i]).subtract(odds[i]);
            }
        }
        return ret;
    }

    public static void main(String[] args) {
        Complex[] in = new Complex[10];
        for (int i = 0; i < 10; i++) {
            in[i] = new Complex(0);
        }

        Complex[] res = fft(in);
        for (int i = 0; i < 10; i++) {
            System.out.println(res[i].toString());
        }
    }
}

