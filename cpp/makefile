all :
	g++ -O2 -march=native -mtune=native -std=c++11 -o a.out *.cpp

run : a.out
	./a.out

test : a.out
	./a.out < ../tests/inputs/alternating.txt > output_alternating.txt
	./a.out < ../tests/inputs/ones.txt > output_ones.txt
	./a.out < ../tests/inputs/zeros.txt > output_zeros.txt
	./a.out < ../tests/inputs/freq_data.txt > output_freq_data.txt