from day import Day
from pt import pt
from itertools import combinations


def parse(lines: list[str]) -> dict[str, set[pt]]:
    pts = {}
    for j, l in enumerate(lines):
        for i, c in enumerate(l):
            if c.isalnum():
                l = pts.get(c, set())
                l.add(pt(i, j))
                pts[c] = l
    return pts


def find_antinodes(m, pts) -> set[pt]:
    pairs = combinations(pts, 2)
    ants = set()
    for a, b in pairs:
        b_to_a = a.sub(b)
        q = a.add(b_to_a)
        if q.within(m):
            ants.add(q)
        q = b.sub(b_to_a)
        if q.within(m):
            ants.add(q)
    return ants


def p1(lines: list[str]) -> int:
    pts = parse(lines)

    # Go frequency by frequency
    # we want to consider all pairs
    ants = set()
    for freq, freq_pts in pts.items():
        freq_ants = find_antinodes(lines, freq_pts)
#        print(freq_ants)
        ants = ants.union(freq_ants)

    return len(ants)


if __name__ == "__main__":
    d = Day(8)
    lines = d.read_lines()
    print(p1(lines))
