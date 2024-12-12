from day import Day, flatten
from pt import pt, NESW

def region_sides(m: list[str], r: set[pt]) -> int:
    v = pt(0,0) in r
    v = False
    # Approach:
    # - decompose into vertical rectangles
    #   - one or more per x value
    # - work from left
    # - first rectangle has 4 edges
    # - adding new rectangle adds 4 edges
    # - overlap with rectangles to the left reduces some edges
    #   - case analysis
    #
    xmin = min([p.x for p in r])
    xmax = max([p.x for p in r])
    slices = []
    for x in range(xmin, xmax+1):
        s = [p for p in r if p.x == x]
        s.sort(key = lambda p: p.y)
#        if v:
#            print(s)
        slices.append(s)

    def slice_to_rects(s: list[pt]) -> list[list[pt]]:
        rects = [[s[0]]]
        for p in s[1:]:
            if p.y != rects[-1][-1].y + 1:
                rects.append([])
            rects[-1].append(p)
        return rects

    slice_rects = [slice_to_rects(s) for s in slices]
    num_edges = 4 * len(slice_rects[0])
    for i, prev_slice in enumerate(slice_rects):
        if i == len(slice_rects) - 1:
            break
        for b in slice_rects[i+1]:
            if v:
                print(f'Adding b {b}')
            num_edges += 4
            for a in prev_slice:
                if v:
                    print(f'Comparing a {a}')
                #
                # +4 for the new rect
                #
                # but:
                # A    B  A   AB   B A   B AB A  AB  B
                # AB  AB  AB  AB  AB A   B AB A  AB  B
                # AB  AB  AB  AB  AB A  A  A  AB  B AB
                # A   AB  AB  AB   B  B A  A  AB  B AB
                #     A    B          B A
                #
                # -0  -0  -0  -4  -0 -0 -0 -2 -2 -2 -2
                #
                if a[0].y == b[0].y:
                    if v:
                        print('-2 edges')
                    num_edges -= 2
                if a[-1].y == b[-1].y:
                    if v:
                        print('-2 edges')
                    num_edges -= 2
#                if a[0].y == b[0].y and a[-1].y == b[-1].y:
#                    num_edges -= 4
#                elif a[0].y == b[0].y and a[-1].y != b[-1].y:
#                    num_edges -= 2
#                elif a[0].y != b[0].y and a[-1].y == b[-1].y:
#                    num_edges -= 2
                if v:
                    print(num_edges, a, b, "\n")


    return num_edges


def region_score_p2(m: list[str], r: set[pt]) -> int:
    area = len(r)
    sides = region_sides(m, r)
#    print(area, sides)
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
# 816883 too low
# 824218 wrong
def p2(lines: list[str]) -> int:
    regions = find_regions(lines)
    return sum([region_score_p2(lines, r) for r in regions])

if __name__ == "__main__":
    d = Day(12)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
