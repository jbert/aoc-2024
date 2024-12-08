from day import Day
from pt import pt
from itertools import combinations
import math


def parse(lines: list[str]) -> dict[str, set[pt]]:
    pts = {}
    for j, l in enumerate(lines):
        for i, c in enumerate(l):
            if c.isalnum():
                l = pts.get(c, set())
                l.add(pt(i, j))
                pts[c] = l
    return pts


def find_antinodes_p2(m, pts) -> set[pt]:
    pairs = combinations(pts, 2)
    ants = set()
    for a, b in pairs:
        b_to_a = a.sub(b)
        factor = math.gcd(b_to_a.x, b_to_a.y)
        step = pt(b_to_a.x / factor, b_to_a.y / factor)
        q = a
        while q.within(m):
            ants.add(q)
            q = q.add(step)
        q = a
        while q.within(m):
            ants.add(q)
            q = q.sub(step)
    return ants


def find_antinodes_p1(m, pts) -> set[pt]:
    pairs = combinations(pts, 2)
    ants = set()
    for a, b in pairs:
        b_to_a = a.sub(b)
        for q in [a.add(b_to_a), b.sub(b_to_a)]:
            if q.within(m):
                ants.add(q)
    return ants


def p2(lines: list[str]) -> int:
    pts = parse(lines)

    ants = set()
    for _, freq_pts in pts.items():
        freq_ants = find_antinodes_p2(lines, freq_pts)
        ants = ants.union(freq_ants)

    return len(ants)


def p1(lines: list[str]) -> int:
    pts = parse(lines)

    ants = set()
    for _, freq_pts in pts.items():
        freq_ants = find_antinodes_p1(lines, freq_pts)
        ants = ants.union(freq_ants)

    return len(ants)


if __name__ == "__main__":
    d = Day(8)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
