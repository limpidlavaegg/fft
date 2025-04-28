import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Executable;
import java.util.*;
import java.util.stream.Collectors;
import org.apache.commons.math3.complex.*;

public class Solution {

    static Complex[] fft(Complex[] in) {
        // NOTE: in must be an even length
        int n = in.length;
        // Base case: in contains just one element -> the result of the transform is the element itself
        if (n == 1) {
            return in;
        }

        // Split array into odd and even indices for divide and conquer
        int half_n = n / 2;
        // Init arrays for storing values at the odd and even indices
        Complex[] odds = new Complex[half_n];
        Complex[] evens = new Complex[half_n];
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
        Complex[] ret = new Complex[n];
        for (int i = 0; i < half_n; i++) {
            // Calc. twiddle factor: exp(-2im*pi*i/n)
            Complex factor = new Complex(0, (-2.0 * Math.PI * i) / n);
            factor = factor.exp().multiply(odds[i]);
            // Front half of the result: evens_i + exp(-2im*pi*i/n) * odds_i
            ret[i] = evens[i].add(factor);
            // Back half of the result: evens_i - exp(-2im*pi*i/n) * odds_i
            ret[i + half_n] = evens[i].subtract(factor);
        }
        return ret;
    }

    static boolean isPowerOfTwo(int n) {
        return (n > 0) && ((n & (n-1)) == 0);
    }

    static String getNote(double freq) {
        String[] notes = {"A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"};
        int num = Math.round(12*Math.log(freq / 55)/Math.log(2)) % 12;
        return notes[num];
    }

    public static void main(String[] args) {
        try {
            BufferedReader r = new BufferedReader(new InputStreamReader(System.in));
            String[] params = r.readLine().split(" ");
            if (params.length != 3) {
                throw new Exception("First line should have 3 integer arguments");
            }
            int n = Integer.parseInt(params[0]);
            int m = Integer.parseInt(params[1]);
            int t = Integer.parseInt(params[2]);
            if (!isPowerOfTwo(m)) {
                throw new Exception("Second argument needs to be power of 2");
            }
            for (int i = 0; i < n; i++) {
                String[] sData = r.readLine().split(" ");
                if (sData.length != m) {
                    throw new Exception("Line " + i + " should have " + m + " arguments");
                }
                Complex[] nData = new Complex[m];
                for (int j = 0; j < m; j++) {
                    nData[j] = new Complex(Double.parseDouble(sData[j]));
                }
                Complex[] trans = fft(nData);

            }    
        } catch (Exception e) {
            System.err.println(e.getMessage());
            System.exit(-1);
        }
    }
}
