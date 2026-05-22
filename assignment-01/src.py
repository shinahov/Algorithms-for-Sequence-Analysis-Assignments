# Run with:
# python src.py AA input.txt

import sys

def shift_or(pattern, text):
    m = len(pattern)
    mask = {}
    bit = 1
    # create the bitmask table for pattern
    for c in pattern:
        if c not in mask:
            mask[c] = 0
        mask[c] |= bit
        bit <<= 1
    # create the full 1s bitmask with m bits to invert the mask values
    full = (1 << m) - 1
    for c in mask:
        mask[c] = full ^ mask[c]
    accept = 1 << (m - 1) # mask for the accepting state
    D = full # initial state with all bits set to 1
    i = 0
    for c in text:
        D = (D << 1) | mask.get(c, full) # shift left and apply the mask for the current character
        if (D & accept) == 0: # if the accepting state is reached
            yield i - m + 1 # yield the starting index of the match
        i += 1
    
def __main__():
    pattern = sys.argv[1]
    filename = sys.argv[2]
    with open(filename, "r", encoding="utf-8") as f:
        inhalt = f.read()
    result = ",".join(str(i) for i in shift_or(pattern, inhalt))
    print(result)

if __name__ == "__main__":
    __main__()