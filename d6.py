from day import Day
from pt import pt, NESW


def parse(lines: list[str]) -> tuple[pt, set[pt]]:
    guard = None
    obs: list[pt] = []
    for j, line in enumerate(lines):
        for i, c in enumerate(line):
            if c == '#':
                obs.append(pt(i, j))
            elif c == '^':
                if not guard is None:
                    raise RuntimeError("more than one guard")
                guard = pt(i, j)
    if guard is None:
        raise RuntimeError("no guard")
    return guard, set(obs)


def p1(lines: list[str]) -> int:
    guard, obs = parse(lines)
#    print(guard)
#    print(obs)
    dirs = NESW
    dir = 0
    visited = set()
    while guard.within(lines):
        visited.add(guard)
        next = guard.add(dirs[dir])
        if next in obs:
            dir = (dir + 1) % len(dirs)
        else:
            guard = next

    return len(visited)


if __name__ == "__main__":
    d = Day(6)
    lines = d.read_lines()
    print(p1(lines))
