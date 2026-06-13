import sys


class Wavefront:
    def __init__(self, from_diag, to_diag):
        self.from_diag = from_diag
        self.to_diag = to_diag
        self.wavefront = [None] * (self.to_diag - self.from_diag + 1)

    def idx(self, k):
        return k - self.from_diag

    def update_furthest_point(self, k, j):
        if not (self.from_diag <= k <= self.to_diag):
            return

        idx = self.idx(k)
        old = self.wavefront[idx]

        if old is None or j > old:
            self.wavefront[idx] = j

    def get_furthest_point(self, k):
        if self.from_diag <= k <= self.to_diag:
            return self.wavefront[self.idx(k)]
        return None

    def items(self):
        result = []
        for k in range(self.from_diag, self.to_diag + 1):
            j = self.get_furthest_point(k)
            if j is not None:
                result.append((k, j))
        return result


def extend_matches(pattern, text, k, j):
    while j - k < len(pattern) and j < len(text) and pattern[j - k] == text[j]:
        j += 1

    return j


def extend_wavefront(pattern, text, wavefront):
    for k, j in wavefront.items():
        new_j = extend_matches(pattern, text, k, j)
        wavefront.update_furthest_point(k, new_j)


def reached_target(pattern, text, wavefront):
    target_diag = len(text) - len(pattern)
    target_offset = len(text)

    j = wavefront.get_furthest_point(target_diag)

    return j is not None and j >= target_offset


def wfa(pattern, text, mismatch_cost, gap_cost):
    # init empty wave
    w0 = Wavefront(0, 0)
    w0.update_furthest_point(0, 0)
    extend_wavefront(pattern, text, w0)
    # init empty dict
    wavefronts = {}
    wavefronts[0] = w0

    score = 1

    while True:
        # check if we can create new wave
        has_missmatch_score = score - mismatch_cost in wavefronts
        has_gap_score = score - gap_cost in wavefronts

        # cant create new wave
        if not has_missmatch_score and not has_gap_score:
            score += 1
            continue

        # create new wave
        max_diag = score // gap_cost
        new_w = Wavefront(-max_diag, max_diag)

        if has_missmatch_score:
            # get wave from where we can allow missmatch
            source_w = wavefronts[score - mismatch_cost]

            for k, j in source_w.items():
                i = j - k
                if i < len(pattern) and j < len(text):
                    # update the wave now from j +1 using missmatch
                    new_w.update_furthest_point(k, j + 1)

        if has_gap_score:
            # get wave from where we can gap
            source_w = wavefronts[score - gap_cost]

            for k, j in source_w.items():
                i = j - k

                if i < len(pattern):
                    # gap in vertikal (down)
                    new_w.update_furthest_point(k - 1, j)

                if j < len(text):
                    # gap in horizontal (right)
                    new_w.update_furthest_point(k + 1, j + 1)

        extend_wavefront(pattern, text, new_w)

        if len(new_w.items()) == 0:
            score += 1
            continue

        wavefronts[score] = new_w
        # reached right down corner
        if reached_target(pattern, text, new_w):
            return score, new_w, wavefronts, max_diag

        score += 1


if __name__ == "__main__":
    input_file = sys.argv[1]
    mismatch_cost = int(sys.argv[2])
    gap_cost = int(sys.argv[3])

    with open(input_file, "r") as f:
        pattern = f.readline().strip()
        text = f.readline().strip()

    score, last_wavefront, ws, max_diag = wfa(pattern, text, mismatch_cost, gap_cost)
    min_diag = -max_diag
    # print(last_wavefront.wavefront.items())
    print("Alignment score: ", score)
    merged = []

    for k in range(last_wavefront.from_diag, last_wavefront.to_diag + 1):
        value = last_wavefront.get_furthest_point(k)
        # print(value)

        if value is None:
            for old_score in sorted(ws.keys(), reverse=True):
                old_w = ws[old_score]
                value = old_w.get_furthest_point(k)

                if value is not None:
                    break

        merged.append((k, value))

    print("Last wavefront:")
    for k, value in merged:
        if k < 0:
            print("   ", k, ": ", value)
        else:
            print("    ", k, ": ", value)
