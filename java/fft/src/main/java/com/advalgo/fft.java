package com.advalgo;

import org.apache.commons.math3;

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

    public static double[] fft(double[] in) {
        // NOTE: in must be an even length
        int n = in.length;
        int half_n = n / 2;

        // Split array into odd and even indices for divide and conquer
        double[] odds = new double[half_n];
        double[] evens = new double[half_n];
        for (int i = 0; i < n; i++) {
            if (i % 2 == 0) {
                evens[i] = in[i];
            }
            else {
                odds[i] = in[i];
            }
        }

        // 
    }

    public static void main(String[] args) {
        System.out.println("hello world");
    }
}

