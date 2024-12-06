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


def p2(lines: list[str]) -> int:
    print('p2')
    guard, obs = parse(lines)
    # p1 took 5344 steps, but we may get longer paths
    max_steps = 130 * 130   # 16900
    loopers = set()
    for j, line in enumerate(lines):
        print(f'j {j}')
        for i, c in enumerate(line):
            o = pt(i, j)
            if o in obs or o == guard:
                continue
            oset = obs.copy()
            oset.add(o)
            visited, steps = simulate(guard, oset, max_steps)
            if steps == max_steps:
                loopers.add(o)

    return len(loopers)


def p1(lines: list[str]) -> int:
    guard, obs = parse(lines)
    visited, steps = simulate(guard, obs)
    return len(visited)


def simulate(guard: pt, obs: set[pt], max_steps=None) -> tuple[set[pt], int]:
    #    print(guard)
    #    print(obs)
    dirs = NESW
    dir = 0
    visited = set()
    steps = 0
    while guard.within(lines):
        visited.add(guard)
        next = guard.add(dirs[dir])
        if next in obs:
            dir = (dir + 1) % len(dirs)
        else:
            guard = next
        steps += 1
        if max_steps is not None:
            if steps >= max_steps:
                break

#    print(f'steps {steps}')
    return visited, steps


if __name__ == "__main__":
    d = Day(6)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
