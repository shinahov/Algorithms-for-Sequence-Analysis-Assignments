import sys


def align(s, t):
    m, n = len(s), len(t)
    T = []
    T.append([i for i in range(m + 1)])
    for i in range(1, n + 1):
        T.append([None] * (m + 1))
        T[i][0] = i
        for j in range(1, m + 1):
            T[i][j] = min(
                T[i - 1][j - 1] + (0 if s[j - 1] == t[i - 1] else 1),
                T[i - 1][j] + 1,
                T[i][j - 1] + 1,
            )
    return T


def align_banded(s, t, k):
    INF = 10**9
    m, n = len(s), len(t)
    T = []
    T.append([INF] * (m + 1))

    for j in range(m + 1):
        if abs(0 - j) <= k:
            T[0][j] = j

    for i in range(1, n + 1):
        T.append([INF] * (m + 1))

        if abs(i - 0) <= k:
            T[i][0] = i

        for j in range(1, m + 1):
            if abs(i - j) <= k:
                T[i][j] = min(
                    T[i - 1][j - 1] + (0 if s[j - 1] == t[i - 1] else 1),
                    T[i - 1][j] + 1,
                    T[i][j - 1] + 1,
                )

    return T


def backtrace(dp_table, s, t):
    i = len(dp_table) - 1
    j = len(dp_table[0]) - 1
    str_i = ""
    str_j = ""

    while i > 0 or j > 0:

        if dp_table[i - 1][j - 1] <= dp_table[i - 1][j]:
            if dp_table[i - 1][j - 1] <= dp_table[i][j - 1]:
                str_i = s[j - 1] + str_i
                str_j = t[i - 1] + str_j
                i = i - 1
                j = j - 1
            else:
                str_i = s[j - 1] + str_i
                str_j = "-" + str_j
                j = j - 1
        else:
            if dp_table[i - 1][j] < dp_table[i][j - 1]:
                str_i = "-" + str_i
                str_j = t[i - 1] + str_j
                i = i - 1
            else:
                str_i = s[j - 1] + str_i
                str_j = "-" + str_j
                j = j - 1

    return str_i, str_j


filename = sys.argv[1]
k = int(sys.argv[2])

with open(filename, "r") as file:
    input = list(file.read().split("\n"))

s = input[0]
t = input[1]


table = align(s, t)
str_i, str_j = backtrace(table, s, t)

print(f"Non-banded edit distance: {table[-1][-1]}")
print("Non-banded alignment:")
print(str_i)
print(str_j)
print("\n")

if abs(len(s) - len(t)) > k:
    print(f"No banded alignment available. Strings differ by length greater than k={k}")
else:
    table_banded = align_banded(s, t, k)
    if table_banded is not None:
        str_i, str_j = backtrace(table_banded, s, t)

        print(f"Banded edit distance: {table_banded[-1][-1]}")
        print("Banded alignment:")
        print(str_i)
        print(str_j)
