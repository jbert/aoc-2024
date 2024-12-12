import os
from typing import TypeVar, Callable
from functools import reduce


class Day:
    def __init__(self, day: int):
        self.day = day
        self.suffix = ""
        test = os.getenv('AOC_TEST')
        if test == "true":
            self.suffix = "-test"
        elif test is not None:
            self.suffix = f'-{test}'

    def _data_path(self):
        return f'data/d{self.day}{self.suffix}.txt'

    def read_lines(self):
        with open(self._data_path(), "r") as f:
            return [line.rstrip() for line in f]


# Space separated integers to list
def str_to_nums(s: str, sep=' ') -> list[int]:
    s = s.strip()
    bits = s.split(sep)
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


T = TypeVar("T")


def freq_count(l: list[T]) -> dict[T, int]:
    def step(acc, c):
        v = acc.get(c, 0)
        acc[c] = v+1
        return acc
    return reduce(step, l, {})


def flatten(l: list[list[T]]) -> list[T]:
    return [x for xs in l for x in xs]


def partition(pred: Callable[[T], bool], l: list[T]) -> tuple[list[T], list[T]]:
    ts = []
    fs = []
    for x in l:
        if pred(x):
            ts.append(x)
        else:
            fs.append(x)
    return ts, fs


def split_list(pred: Callable[[T], bool], l: list[T]) -> list[list[T]]:
    chunks = []
    chunk = []
    for t in l:
        if pred(t):
            chunks.append(chunk)
            chunk = []
        else:
            chunk.append(t)

    chunks.append(chunk)
    return chunks
