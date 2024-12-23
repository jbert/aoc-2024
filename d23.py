from day import Day


def parse(lines: list[str]) -> tuple[set[str], dict[str, set[str]], set[tuple[str, str]]]:
    neighbours: dict[str, set[str]] = {}
    verts = set()
    edges = set()
    for line in lines:
        bits = line.split('-')
        a, b = bits[0], bits[1]
        verts.add(a)
        verts.add(b)
        l = neighbours.get(a, set())
        l.add(b)
        neighbours[a] = l

        l = neighbours.get(b, set())
        l.add(a)
        neighbours[b] = l

        edges.add((a, b))
        edges.add((b, a))

    return verts, neighbours, edges


def p1(lines: list[str]) -> int:
    verts, neighbours, edges = parse(lines)
#    print(verts)
#    print(neighbours)
#    print(edges)
    triples: set[tuple[str, str, str]] = set()
    for p in verts:
        ns = neighbours[p]
        for u in ns:
            for v in ns:
                if (u, v) in edges:
                    l = sorted([p, u, v])
                    triples.add((l[0], l[1], l[2]))
#    print(triples)

    def has_t(t):
        return t[0][0] == 't' or t[1][0] == 't' or t[2][0] == 't'

#    print([t for t in triples if has_t(t)])
    return len([t for t in triples if has_t(t)])


if __name__ == "__main__":
    d = Day(23)
    lines = d.read_lines()
    print(p1(lines))
