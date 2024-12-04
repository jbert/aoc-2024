from day import Day
from pt import pt, ALL_DIRS, matrix_bounds


def is_xmas(p: pt, m: list[str]) -> bool:
    dirs = [dir for dir in ALL_DIRS if p.add(dir.scale(3)).within(m)]
#    print(f'p {p} dirs {dirs} m_bounds {matrix_bounds(m)}')

    def is_dir(p, dir) -> bool:
        for i, c in enumerate('XMAS'):
            if p.add(dir.scale(i)).char_at(m) != c:
                return False
        return True

    return len([dir for dir in dirs if is_dir(p, dir)]) > 0


def p1(lines: list[str]) -> int:
    xs = [pt(i, j) for j, l in enumerate(lines)
          for i, c in enumerate(l) if c == 'X']
    # print(is_xmas(xs[0], lines))
    xmass = [x for x in xs if is_xmas(x, lines)]
    print(xmass)
    return len(xmass)


if __name__ == "__main__":
    d = Day(4)
    lines = d.read_lines()
    print(p1(lines))
