import os


class Day:
    def __init__(self, day: int, test=None):
        self.day = day
        if test is None:
            test = os.getenv('AOC_TEST') == "true"
        self.test = test

    def _data_path(self):
        suffix = "-test" if self.test else ""
        return f'data/d{self.day}{suffix}.txt'

    def read_lines(self):
        with open(self._data_path(), "r") as f:
            return [line.rstrip() for line in f]


# Space separated integers to list
def str_to_nums(s: str) -> list[int]:
    s = s.strip()
    bits = s.split(' ')
    return [int(bit) for bit in bits if len(bit) > 0]


# Split on blank lines
def lines_to_chunks(lines: list[str]) -> list[list[str]]:
    # ensure we have terminating empty line
    lines.append("")
    chunks = []
    chunk = []
    for l in lines:
        if l == "":
            chunks.append(chunk)
            chunk = []
        else:
            chunk.append(l)
    return chunks


def range_intersect(a: range, b: range) -> range:
    # Ensure a starts before b
    if a.start > b.start:
        return range_intersect(b, a)

    # AAAAA
    #        BBBB
    if a.stop <= b.start:
        return range(0, 0)

    # AAAAAAAAAAAA
    #    BBBBBBB
    if a.stop >= b.stop:
        return b

    # AAAAAAA
    #    BBBBBBB
    return range(b.start, a.stop)


# Return (A intersection B), [remains of A]
def range_subtract(a: range, b: range) -> tuple[range | None, list[range]]:
    if len(a) == 0 or len(b) == 0:
        raise RuntimeError("Must be non-zero")

    ri = range_intersect(a, b)
    # AAAA
    #        BBBB
    # and
    # BBBB
    #        AAAA
    if len(ri) == 0:
        # print("JB1")
        return (None, [a])

    #    AAAA
    # BBBBBBBBBB
    if ri.start == a.start and ri.stop == a.stop:
        # print("JB2")
        return (ri, [])

    # AAAAAAAAAA
    #   BBBBBB
    if ri.start == b.start and ri.stop == b.stop:
        # print("JB3")
        return (ri, [r for r in [range(a.start, b.start), range(b.stop, a.stop)] if (r.stop-r.start) > 0])

    # AAAAAAA
    #    BBBBBB
    if ri.stop == a.stop:
        # print("JB4")
        return (ri, [range(a.start, ri.start)])

    #    AAAAAAA
    # BBBBBB
    if ri.start == a.start:
        # print("JB5")
        return (ri, [range(ri.stop, a.stop)])

    raise RuntimeError(f'Logic error: {a} {b}')


def transpose(M: list[list[int]]) -> list[list[int]]:
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]


def repeat_counts(l):
    last_c = None
    last_count = 0
    counts = {}
    for c in l:
        if last_c is not None:
            if c == last_c:
                last_count += 1
            else:
                counts[last_c] = last_count
                last_c = c
                last_count = 1
        else:
            last_c = c
            last_count = 1
    counts[last_c] = last_count
    return counts
