from day import Day
from pt import pt, ALL_DIRS, NE, SE, SW, NW


def xmas_count(p: pt, m: list[str]) -> int:
    dirs = [dir for dir in ALL_DIRS if p.add(dir.scale(3)).within(m)]

    def good_dir(p, dir) -> bool:
        for i, c in enumerate('XMAS'):
            found = p.add(dir.scale(i)).char_at(m)
            if found != c:
                return False
        return True

    return len([dir for dir in dirs if good_dir(p, dir)])


def p1(lines: list[str]) -> int:
    xs = [pt(i, j) for j, l in enumerate(lines)
          for i, c in enumerate(l) if c == 'X']
    xmas_counts = [xmas_count(x, lines) for x in xs]
    return sum(xmas_counts)


def p2(m: list[str]) -> int:
    As = [pt(i, j) for j, l in enumerate(lines)
          for i, c in enumerate(l) if c == 'A']
    # four directions, if we have an M in one we want an S in the other

    def x_mas_count(a: pt) -> int:
        dirs = [NE, SE, SW, NW]
        return len([dir for dir in dirs if a.sub(dir).char_at(m, '') == 'M' and a.add(dir).char_at(m, '') == 'S'])

    counts = [c for c in [x_mas_count(a) for a in As] if c == 2]
#    print(counts)
    return len(counts)


if __name__ == "__main__":
    d = Day(4)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
