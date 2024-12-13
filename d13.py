from day import Day, split_list
from pt import pt
from typing import NamedTuple

# Press A a times, B b times
#
# Lattice problem


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


def solve_machine(m: machine) -> int:
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
    return sum([solve_machine(m) for m in machines])


if __name__ == "__main__":
    d = Day(13)
    lines = d.read_lines()
    print(p1(lines))
