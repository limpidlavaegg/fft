from math import pi, sin, cos

def dft(X):
    N = len(X)
    roots = [complex(real=cos(-2*pi*k/N), imag=sin(-2*pi*k/N)) for k in range(N)]
    Y = []
    for k in range(N):
        Y.append(sum([X[n] * roots[n*k % N] for n in range(N)]))
    return Y

def fft(X: list[float]) -> list[float]:
    N = len(X)
    if N == 1:
        return X 
    Xodd = []
    Xeven = []
    for i in range(N):
        if i % 2 == 0:
            Xeven.append(X[i])
        else:
            Xodd.append(X[i])
    Yodd = fft(Xodd)
    Yeven = fft(Xeven)
    Y = [0] * N
    arg = -2*pi/N
    for k in range(N//2):
        root = complex(real=cos(arg*k), imag=sin(arg*k))
        Y[k] = Yeven[k] + root*Yodd[k]
        Y[k+N//2] = Yeven[k] - root*Yodd[k]
    return Y

def main():
    X = [2*cos(x) + cos(2*x) for x in range(1024)]
    Yfft = fft(X)
    Ydft = dft(X)
    # for i in range(len(X)):
    #     print(f"{Yfft[i].real}\t{Ydft[i].real}")
    print(all([abs(Yfft[i] - Ydft[i]) <= 1e-5 for i in range(len(Yfft))]))

if __name__=='__main__':
    main()

