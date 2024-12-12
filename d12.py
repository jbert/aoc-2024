from day import Day
from pt import pt, NESW

def region_sides(m: list[str], r: set[pt]) -> int:
    peri = region_peri(m, r, True)
    counts: dict[pt,int] = {}
    for p in peri:
        c = counts.get(p, 0)
        counts[p] = c + 1

    def decr_count(p):
        c = counts[p]
        c -= 1
        counts[p] = c
        if c == 0:
            del counts[p]

    num_edges = 0
    while len(counts) > 0:
        p = list(counts.keys())[0]
        decr_count(p)

        edge = [p]
        num_edges += 1
        for dir in NESW:
            q = p.add(dir)
            if q not in counts:
                continue

            while q in counts:
                decr_count(q)
                edge.append(q)
                q = q.add(dir)

            dir = dir.scale(-1)
            q = p.add(dir)

            if q not in counts:
                continue

            while q in counts:
                decr_count(q)
                edge.append(q)
                q = q.add(dir)
            break


    return num_edges

def region_score_p2(m: list[str], r: set[pt]) -> int:
    area = len(r)
    sides = region_sides(m, r)
    print(area, sides)
    return area * sides


def region_score_p1(m: list[str], r: set[pt]) -> int:
    area = len(r)
    peri = region_peri(m, r, True)
#    print(peri)
    len_peri = len(peri)
#    print(area, len_peri)
    return area * len_peri

# Double-includes points adjacent to more than one region point
# Can collapse with set() or count for perimeter
def region_peri(m: list[str], r: set[pt], include_external=False) -> list[pt]:
    adj = []
    for p in r:
        adj = adj + p.adjacent_pts_nesw()

    def is_adj(p: pt) -> bool:
        return (include_external or p.within(m)) and p not in r

    return list(filter(is_adj, adj))

def flood_find_region(m: list[str], seen: set[pt], p: pt) -> set[pt]:
    c = p.char_at(m)
    r = set([p])
#    print(f'p {p} c {c}')
    added = True
    while added:
        added = False
#        print(f'r {r}')
        # Optimisation: only look at pts added last loop
        border = set(region_peri(m, r))
        border = border - seen
#        print(f'border {border} seen {seen}')
        for b in border:
            if b.char_at(m) == c:
                r.add(b)
                seen.add(b)
                added = True
    return r

def find_regions(m: list[str]) -> list[set[pt]]:
    regions = []
    seen = set()
    for j, l in enumerate(m):
        for i, c in enumerate(l):
            p = pt(i, j)
            if p not in seen:
                r = flood_find_region(m, seen, p)
                regions.append(r)
                seen = seen.union(r)
    return regions

def p1(lines: list[str]) -> int:
    regions = find_regions(lines)
    return sum([region_score_p1(lines, r) for r in regions])

# 1206 right:
# 817964 too low
def p2(lines: list[str]) -> int:
    regions = find_regions(lines)
    return sum([region_score_p2(lines, r) for r in regions])

if __name__ == "__main__":
    d = Day(12)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
