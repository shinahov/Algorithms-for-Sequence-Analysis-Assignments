import sys


def read_fasta(path):
    names, seqs, cur = [], [], []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        if line[0] == ">":
            if names:
                seqs.append("".join(cur))
                cur = []
            names.append(line[1:])
        else:
            cur.append(line)
    if names:
        seqs.append("".join(cur))
    return names, seqs[0], seqs[1]


def sub(a, b, match, mismatch):
    return match if a == b else mismatch


def last_row(a, b, match, mismatch, gap):
    #init first row
    prev = [j * gap for j in range(len(a) + 1)]

    for i, cb in enumerate(b, 1):
        cur = [i * gap] + [0] * len(a)
        
        # compute row
        for j, ca in enumerate(a, 1):
            cur[j] = max(
                prev[j - 1] + sub(ca, cb, match, mismatch),
                prev[j] + gap,
                cur[j - 1] + gap,
            )
        # in memory only last 2 rows
        prev = cur

    return prev


def nw(a, b, match, mismatch, gap):
    dp = [[0] * (len(a) + 1) for _ in range(len(b) + 1)]

    for j in range(1, len(a) + 1):
        dp[0][j] = dp[0][j - 1] + gap

    for i in range(1, len(b) + 1):
        dp[i][0] = dp[i - 1][0] + gap

    for i in range(1, len(b) + 1):
        for j in range(1, len(a) + 1):
            dp[i][j] = max(
                dp[i - 1][j - 1] + sub(a[j - 1], b[i - 1], match, mismatch),
                dp[i - 1][j] + gap,
                dp[i][j - 1] + gap,
            )

    i, j = len(b), len(a)
    aa, bb = [], []

    while i or j:
        if (
            i
            and j
            and dp[i][j] == dp[i - 1][j - 1] + sub(a[j - 1], b[i - 1], match, mismatch)
        ):
            aa.append(a[j - 1])
            bb.append(b[i - 1])
            i -= 1
            j -= 1
        elif i and dp[i][j] == dp[i - 1][j] + gap:
            aa.append("-")
            bb.append(b[i - 1])
            i -= 1
        else:
            aa.append(a[j - 1])
            bb.append("-")
            j -= 1

    return "".join(reversed(aa)), "".join(reversed(bb))


def hirschberg(a, b, match, mismatch, gap):
    #end of recursion 
    if len(a) == 1 or len(b) == 1:
        return nw(a, b, match, mismatch, gap)

    #split the string
    mid = len(b) // 2

    left = last_row(a, b[:mid], match, mismatch, gap)
    right = last_row(a[::-1], b[mid:][::-1], match, mismatch, gap)

    
    k = max(range(len(a) + 1), key=lambda j: left[j] + right[len(a) - j])

    a1, b1 = hirschberg(a[:k], b[:mid], match, mismatch, gap)
    a2, b2 = hirschberg(a[k:], b[mid:], match, mismatch, gap)

    return a1 + a2, b1 + b2


def score(a, b, match, mismatch, gap):
    total = 0

    for x, y in zip(a, b):
        if x == "-" or y == "-":
            total += gap
        else:
            total += sub(x, y, match, mismatch)

    return total


def main():
    infile = sys.argv[1]
    outfile = sys.argv[2]
    match, mismatch, gap = map(int, sys.argv[3:6])

    names, a, b = read_fasta(infile)

    aa, bb = hirschberg(a, b, match, mismatch, gap)

    with open(outfile, "w") as f:
        f.write(f">{names[0]}\n{aa}\n>{names[1]}\n{bb}\n")

    print(score(aa, bb, match, mismatch, gap))


if __name__ == "__main__":
    main()
