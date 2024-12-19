from day import Day


def parse(lines: list[str]) -> tuple[list[str], list[str]]:
    avail = sorted(lines[0].split(', '), key=lambda s: len(s), reverse=True)
    return avail, lines[2:]


def range_touch(a: range, b: range) -> bool:
    if a.start > b.start:
        return range_touch(b, a)
    return a.stop >= b.start


def range_join(a: range, b: range) -> range:
    if a.start > b.start:
        return range_join(b, a)
    if not range_touch(a, b):
        raise RuntimeError(f"can't join disjoint ranges {a} {b}")
    return range(a.start, b.stop)


def all_ranges(d, p) -> list[range]:
    ld = len(d)
    lp = len(p)
    rs = []
    for i in range(ld):
        if i + lp > ld:
            break
        if d[i:i+lp] == p:
            rs.append(range(i, i+lp))
    return rs


def is_possible(design, patterns) -> bool:
    covers: dict[str, list[range]] = {}
    for p in patterns:
        covers[p] = all_ranges(design, p)
    icovers: list[list[range]] = [[] for _ in range(len(design))]
    for _, rs in covers.items():
        for r in rs:
            icovers[r.start].append(r)
#    print(design)
#    print(covers)
#    print(icovers)
    return is_covered(range(len(design)), icovers)


def calc_icovers(design, patterns) -> list[list[range]]:
    covers: dict[str, list[range]] = {}
    for p in patterns:
        covers[p] = all_ranges(design, p)
    icovers: list[list[range]] = [[] for _ in range(len(design))]
    for _, rs in covers.items():
        for r in rs:
            icovers[r.start].append(r)
    return icovers


def find_cover(dr: range, icovers: list[list[range]]) -> list[range] | None:
    #    print(f'FC {dr} {icovers}')
    if len(dr) == 0:
        # print("JB1")
        return []
    if len(icovers) == 0:
        # print("JB2")
        return None
    zero_ranges = icovers[0]
    for zr in zero_ranges:
        # print(f'zr {zr}')
        cover = find_cover(range(zr.stop, dr.stop), icovers[len(zr):])
        if cover is not None:
            # print("JB3")
            return [zr] + cover
    # print("JB5")
    return None


def solve(design, patterns) -> list[str] | None:
    icovers = calc_icovers(design, patterns)
    soln = find_cover(range(len(design)), icovers)
#    print(f'd {design} soln {soln}')
    if soln is None:
        return None
    return [design[r.start:r.stop] for r in soln]


cache: dict[str, int] = {}


def count_covered(dr: range, icovers: list[list[range]]) -> int:
    k = f'{dr} {icovers}'
    global cache
    v = cache.get(k, None)
    if v is not None:
        return v

#    print(f'cc {dr} icovers {icovers}')
    if len(dr) == 0:
        # print(f'JB0 1')
        cache[k] = 1
        return 1
    if len(icovers) == 0:
        # print(f'JB1 0')
        cache[k] = 0
        return 0
    zero_ranges: list[range] = icovers[0]
    total = 0
    for zr in zero_ranges:
        # print(f'zr {zr}')
        n = count_covered(range(zr.stop, dr.stop), icovers[len(zr):])
        # print(f'JB2 {n}')
        total += n
    # print(f'JB3 {total}')
    cache[k] = total
    return total


def is_covered(dr: range, icovers: list[list[range]]) -> bool:
    #    print(f'ic {dr} icovers {icovers}')
    if len(dr) == 0:
        #    print(f'JB0 True')
        return True
    if len(icovers) == 0:
        # print(f'JB1 False')
        return False
    zero_ranges = icovers[0]
    for zr in zero_ranges:
        if is_covered(range(zr.stop, dr.stop), icovers[len(zr):]):
            #    print(f'JB2 True')
            return True
    # print(f'JB3 False')
    return False

# 241 - passes test, too high
# 129 - too low
# 241 - on both methods, with covers


def p1(lines: list[str]) -> int:
    patterns, designs = parse(lines)
    #    print(avail)
    #    print(designs)
    possible = 0
    for d in designs:
        #    for d in ['brwrr']:
        # for d in ['wbrwwrurggrwuugbuurubbwwugwuuurwrggwgrruuubggwbwrbr']:
        soln = solve(d, patterns)
        ip = is_possible(d, patterns)
        if ip != (soln is not None):
            print(f'd: {d} BAD: disagreement {ip} {soln}')
            continue
        if soln is not None:
            soln_d = "".join(soln)
            if d != soln_d:
                print(f'd: {d} BAD join\n{d}\n{soln_d}')
            possible += 1
            for p in soln:
                if p not in patterns:
                    print(f'd: {d} BAD pattern {p}')
#        print(f'd {d} {soln}')
#        print(f'd: {d} {is_possible(d, patterns)}')
#    return len([d for d in designs if is_possible(d, patterns)])
    return possible


def p2(lines: list[str]) -> int:
    global cache
    patterns, designs = parse(lines)
    total = 0
    for d in designs:
        #    for d in ['ggrggugwgrrrggrruggurggwguuuuubwrurbgrgbwwwuurg']:
        icovers = calc_icovers(d, patterns)
        cache = {}
        n = count_covered(range(len(d)), icovers)
    #    print(f'd {d} count {n}')
        if d is not None:
            total += n
    return total


if __name__ == "__main__":
    d = Day(19)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
