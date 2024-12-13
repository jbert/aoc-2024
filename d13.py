from day import Day, split_list
from pt import pt, mat
from typing import NamedTuple

# Press A na times, B nb times
# vectors are a and b
#
# Just x axis:
#
# a = 94
# b = 22


class machine(NamedTuple):
    a: pt
    b: pt
    prize: pt


def parse_button(s: str) -> pt:
    bits = s.split(' ')
    x = int(bits[2][2:-1])
    y = int(bits[3][2:])
    return pt(x, y)


def parse_machine(l: list[str]) -> machine:
    a = parse_button(l[0])
    b = parse_button(l[1])
    bits = l[2].split(' ')
    x = int(bits[1][2:-1])
    y = int(bits[2][2:])
    prize = pt(x, y)
    return machine(a, b, prize)


def parse(lines: list[str]) -> list[machine]:
    chunks = split_list(lambda l: l == "", lines)
    return [parse_machine(chunk) for chunk in chunks]


def solve_machine_p1(m: machine) -> int:
    # na is A count, na is B count
    # Want to search (na, nb) in (0,0) -> (100,100) space
    # but can stop search on each once we exceed
    for na in range(0, 101):
        for nb in range(0, 101):
            if m.a.scale(na).add(m.b.scale(nb)) == m.prize:
                #                print(na, nb)
                return 3 * na + nb
    return 0


def p1(lines: list[str]) -> int:
    machines = parse(lines)
#    print([solve_machine(m) for m in machines])
    return sum([solve_machine_p1(m) for m in machines])


def element_order(g: int, m: int) -> int:
    n = 1
    total = g
    while True:
        if total % m == 0:
            return n
        total += g
        n += 1


def solve_machine_p2(m: machine) -> int:
    M = mat(m.a.x, m.b.x, m.a.y, m.b.y)
    pp = M.int_inv().times(m.prize)
    invd = M.inv_det()
#    print(invd)
#    print(pp)
    ppx = pp.x / invd
    ppy = pp.y / invd
#    print(ppx, ppy)

    epsilon = 0.00000001
    if ppx - int(ppx) < epsilon and ppy - int(ppy) < epsilon:
        return int(ppx) * 3 + int(ppy)
    return 0


def p2(lines: list[str]) -> int:
    offset = pt(10000000000000, 10000000000000)
#    offset = pt(0, 0)
    machines = [machine(m.a, m.b, m.prize.add(offset))
                for m in parse(lines)]
    # ax mod bx = m
    # m * X == 0 mod bx
    # Y is same for ay mod by
    #
    # Lattice repeats (X, Y), we can subtract enough of those to move it across
    # (then add back the difference)
#    print([solve_machine_p2(m) for m in machines])
    return sum([solve_machine_p2(m) for m in machines])

# 875318608908 too low


if __name__ == "__main__":
    d = Day(13)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
