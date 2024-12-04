from day import Day
from pt import pt, ALL_DIRS


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
#    print(xmas_counts)
    return sum(xmas_counts)


if __name__ == "__main__":
    d = Day(4)
    lines = d.read_lines()
    print(p1(lines))
