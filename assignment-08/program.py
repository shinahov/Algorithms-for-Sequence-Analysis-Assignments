#!/usr/bin/env python3
import sys


class Count_Min:
    def __init__(self, r, w, M, N):
        self.r = r
        self.w = w
        self.M = M
        self.N = N
        # init empty matrix
        self.matrix = [[0] * w for _ in range(r)]

    def h0(self, c):
        return ord(c) * self.M % self.w

    def h1(self, c):
        return ((self.N << 5) + self.N + ord(c)) % self.w

    def hi(self, c, i):
        return (self.h0(c) + i * self.h1(c)) % self.w

    def compute_matrix(self, pattern):
        for char in pattern:
            # for every char compute it hash value for each hash function
            for row in range(len(self.matrix)):
                col = self.hi(char, row)
                self.matrix[row][col] += 1

    def get_min(self, char):
        count = []
        # collect all matrix entrys that char hashes to and get min
        for row in range(len(self.matrix)):
            col = self.hi(char, row)
            count.append(self.matrix[row][col])
        return min(count)


if __name__ == "__main__":

    input_file = sys.argv[1]
    input_r = int(sys.argv[2])
    input_w = int(sys.argv[3])
    input_M = int(sys.argv[4])
    input_N = int(sys.argv[5])
    input_char = sys.argv[6]
    with open(input_file, "r") as f:
        pattren = f.readline().strip()
    cm = Count_Min(input_r, input_w, input_M, input_N)
    cm.compute_matrix(pattren)
    print(cm.get_min(input_char))
