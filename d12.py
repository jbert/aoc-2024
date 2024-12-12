from day import Day
from pt import pt

def region_score(m: list[str], r: set[pt]) -> int:
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
    return sum([region_score(lines, r) for r in regions])

if __name__ == "__main__":
    d = Day(12)
    lines = d.read_lines()
    print(p1(lines))
