from math import pi, sin, cos

def fft(X: list[float]) -> list[float]:
    N = len(X)

    # Base case: in contains just one element -> the result of the transform is the element itself
    if N == 1:
        return X 
    
    # Split array into odd and even indices to calculate a DFT via divide-and-conquer
    Xodd = []
    Xeven = []
    for i in range(N):
        if i % 2 == 0:
            Xeven.append(X[i])
        else:
            Xodd.append(X[i])

    # Recursively calculate the DFT on odds and evens separately, we will merge the results below
    Yodd = fft(Xodd)
    Yeven = fft(Xeven)

    # Init an array of all 0s of size N to store the results of the merge operation
    Y = [0] * N
    # Define constant value for use in calculating the twiddle factors
    arg = -2*pi/N
    for k in range(N//2):
        # Calculate the twiddle factor: exp(-2im*pi*k/n)
        # This approach to calculating the twiddle factor uses sine and cosine waves to define the real and imaginary components of the factor, respectively, rather than taking the complex exponential. However, the two approaches are equivalent
        root = complex(real=cos(arg*k), imag=sin(arg*k))
        # Front half of the result: even_k + exp(-2im*pi*k/n) * odd_k
        Y[k] = Yeven[k] + root*Yodd[k]
        # Back half of the result: even_k - exp(-2im*pi*k/n) * odd_k
        Y[k+N//2] = Yeven[k] - root*Yodd[k]
    return Y

def main():
    n = int(input())
    X = list()
    for i in range(n):
        X.append(float(input()))
    
    Y = fft(X)
    for i in range(len(Y)):
        print(f"({Y[i].real:0,.5f}, {Y[i].imag:0,.5f})")
        

if __name__=='__main__':
    main()

