from copyreg import add_extension
from day import Day, flatten
from pt import pt


def p1(m: list[str]) -> int:
    letters = {}

    def adjacent_set(ps: set[pt]) -> set[pt]:
        return set(flatten([p.adjacent_pts() for p in ps if p.within(m)]))

    for char in 'XMAS':
        letters[char] = set([pt(i, j) for j, l in enumerate(lines)
                             for i, c in enumerate(l) if c == char])

    goodXs = letters['X'].intersection(adjacent_set(letters['M']))
    goodMs = letters['M'].intersection(adjacent_set(goodXs))
    goodAs = letters['A'].intersection(adjacent_set(goodMs))
    goodSs = letters['S'].intersection(adjacent_set(goodAs))

    print(len(goodSs))
    return 0


if __name__ == "__main__":
    d = Day(4)
    lines = d.read_lines()
    print(p1(lines))
