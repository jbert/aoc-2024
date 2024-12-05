from day import Day, str_to_nums


def is_valid(report: list[int], succs) -> bool:
    #    print("R", report)
    for i, b in enumerate(report[1:]):
        a = report[i]
#        print(f'a {a} b {b}')
        if not b in succs[a]:
            return False

    return True


def p1(lines: list[str]) -> int:
    pairs = []
    reports = []
    for i, l in enumerate(lines):
        if l == "":
            reports = [str_to_nums(ll, ',') for ll in lines[i+1:]]
            break
        bits = l.split('|')
        pair = [int(bits[0]), int(bits[1])]
        pairs.append(pair)

    succs: dict[int, set[int]] = {}
    for p in pairs:
        s = succs.get(p[0], set())
        s.add(p[1])
        succs[p[0]] = s

        # Ensure we have at least empty set for RHS
        s = succs.get(p[1], set())
        succs[p[1]] = s

#    print("succes", succs)
#    print([r for r in reports if is_valid(r, succs)])
    return (sum([r[int(len(r)/2)] for r in reports if is_valid(r, succs)]))


if __name__ == "__main__":
    d = Day(5)
    lines = d.read_lines()
    print(p1(lines))
