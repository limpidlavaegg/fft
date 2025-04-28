all :
	g++ -O2 -march=native -mtune=native -std=c++11 -o a.out *.cpp

run : a.out
	./a.out

test : a.out
	./a.out < ../io/sample.in.1 > output_alternating.txt
	./a.out < ../io/sample.in.2 > output_ones.txt
	./a.out < ../io/sample.in.3 > output_zeros.txt
	./a.out < ../io/sample.in.4 > output_freq_data.txt