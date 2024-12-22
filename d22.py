from day import Day
from collections import deque
from collections.abc import Sequence
from itertools import islice, product


def next_num(a: int) -> int:
    a = ((a * 64) ^ a) % 16777216
    a = (int(a / 32) ^ a) % 16777216
    a = ((a * 2048) ^ a) % 16777216
    return a


def sequence(n: int):
    while True:
        yield n
        n = next_num(n)


def prices(seq):
    for s in seq:
        yield s % 10


def deltas(ps):
    last = next(ps)
    for p in ps:
        yield p - last
        last = p


def delta_price(ps: Sequence[int]):
    last = next(ps)
    for p in ps:
        yield (p - last, p)
        last = p

# From itertools recipes:


def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def next_nums(nums: list[int]) -> list[int]:
    return [next_num(n) for n in nums]

#
#
# def next_nums_to(nums: list[int], upto: int):
#    yield nums
#    for _ in range(upto):
#        nums = next_nums(nums)
# print(f'NN {nums}')
#        yield nums
#
#
# def prices_to(nums: list[int], upto: int):
#    for nums in next_nums_to(nums, upto):
#        #        xs = [n % 10 for n in nums]
#        #        print(f'PT {xs}')
#        yield [n % 10 for n in nums]
#
#
# def deltas_to(nums: list[int], upto: int):
#    last = []
#    for ps in prices_to(nums, upto):
#        if len(last) != 0:
#            #            xs = [ps[i] - last[i] for i in range(len(ps))]
#            #            print(f'DT {xs}')
#            yield [ps[i] - last[i] for i in range(len(ps))]
#
#        last = ps[:]
#
#
# def four_deltas_to(nums: list[int], upto: int):
#    fours = []
#    for ds in deltas_to(nums, upto):
#        fours = [fours[1:] + [d] for d in ds]
#        if len(fours) == 4:
#            yield fours


def fourmap(prices) -> dict[tuple[int, int, int, int], int]:
    fourmap = {}
    l = []
    for d, p in delta_price(prices):
        #        print(f'd {d} p {p}')
        l.append(d)
        if len(l) < 4:
            continue
        if len(l) > 4:
            l = l[1:]
        t = (l[0], l[1], l[2], l[3])
        fourmap[t] = p
    return fourmap


def all_fours():
    all_ps = product(range(10), range(10), range(10), range(10), range(10))
    for ps in all_ps:
        yield ps[1] - ps[0], ps[2] - ps[1], ps[3] - ps[2], ps[4] - ps[3]


def four_score(fourmaps, fours) -> int:
    total = 0
    for fm in fourmaps:
        p = fm.get(fours, None)
        if p is not None:
            total += p
    return total


# 1858 - too low
# 1881 - too low
def p2(lines: list[str]) -> int:
    nums = [int(l) for l in lines]
    upto = 2000
    #    fours = (-2, 1, -1, 3)

    # nums = [123]
    # upto = 10
    # fours = (-1, -1, 0, 2)

    # nums = [1, 2, 3, 2024]
    # upto = 2000
#    fours = (-2, 1, -1, 3)

    # print(nums)
    price_lists = [prices(islice(sequence(num), upto)) for num in nums]

#    windows = {sliding_window(deltas(p), 4): i for i, p in enumerate(all_prices)]
#    four_sets = [set(list(w)) for i, w in enumerate(windows)]
    fourmaps = [fourmap(ps) for ps in price_lists]
#    print(f'Have {len(fourmaps)} fourmaps')
    best = 0
#    afours = set(list(all_fours()))
    for i, fs in enumerate(all_fours()):
        score = four_score(fourmaps, fs)
        if score > best:
            best = score
            print(f'i {i} fs {fs}: {score}')
    return best


def p1(lines: list[str]) -> int:
    nums = [int(l) for l in lines]
    print(nums)
    for _ in range(2000):
        nums = next_nums(nums)
    #    print(nums)
    return sum(nums)


if __name__ == "__main__":
    d = Day(22)
    lines = d.read_lines()
    #    print(p1(lines))
    print(p2(lines))
