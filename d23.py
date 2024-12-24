from day import Day
from functools import cache


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


conn_cache: dict[int, set[str]] = {}


def set_to_str(ps: set[str]) -> str:
    return ",".join(sorted(list(ps)))


def str_to_set(s: str) -> set[str]:
    return set(s.split(','))


def find_n_connected(n, verts: set[str], neighbours, edges) -> set[str]:
    if n == 1:
        ret: set[str] = verts
        conn_cache[1] = ret
        print(f'ret {len(ret)}')
        return ret

    nmins_str = find_n_connected(n-1, verts, neighbours, edges)

    ret = set()
    for nmin_str in nmins_str:
        nmin = str_to_set(nmin_str)
        rest = verts - nmin
        for r in rest:
            if len(neighbours[r].intersection(nmin)) == len(nmin):
                new = nmin.copy()
                new.add(r)
                ret.add(set_to_str(new))
    conn_cache[n] = ret
#    print(f'ret n {n} {len(ret)} {ret}')
    print(f'ret n {n} {len(ret)}')
    return ret

    # conn_cache: dict[int, list[list[str]]] = {}
    #
    # def find_n_connected(n, verts: set[str], neighbours, edges) -> list[list[str]]:
    #    print(f'n {n}')
    #    if n == 1:
    #        ret: list[list[str]] = [[p] for p in verts]
    #        conn_cache[1] = ret
    #        print(f'ret {len(ret)}')
    #        return ret
    #
    #    nmins = find_n_connected(n-1, verts, neighbours, edges)
    #
    #    ret: list[list[str]] = []
    #    for nmin in nmins:
    #        rest = verts - set(nmin)
    #        for r in rest:
    #            if len(neighbours[r].intersection(nmin)) == len(nmin):
    #                new = list(nmin)
    #                new.append(r)
    #                new = sorted(new)
    #                ret.append(new)
    #    conn_cache[n] = ret
    #    print(f'ret {len(ret)}')
    #    return ret

# Tried 'ao-es-fe-if-in-io-ky-qq-rd-rn-rv-vc-vl'
# D'oh: read the instructions, john. Answer is: 'ao,es,fe,if,in,io,ky,qq,rd,rn,rv,vc,vl'


def p2(lines: list[str]) -> str:
    verts, neighbours, edges = parse(lines)

    # populate cache
    find_n_connected(len(verts), verts, neighbours, edges)
    for n in range(1, len(verts)):
        if len(conn_cache[n]) > 0:
            print(f'n {n} {conn_cache[n]}')
    return ""


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
    print(p2(lines))
