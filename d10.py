from day import Day
from pt import pt, NESW


def parse(lines: list[str]) -> set[pt]:
    starts = set()
    for j, l in enumerate(lines):
        for i, c in enumerate(l):
            if c == '0':
                starts.add(pt(i, j))
    return starts


def trailhead_score(h: pt) -> int:
    # print(h)
    pool = set([h])
    for level in range(0, 9):
        # we have 'level', look for level+1
        want = str(level+1)
        next_pool = set()
        for p in pool:
            # print(f'NP0 {next_pool}')
            poss = p.adjacent_pts_nesw()
            # print(f'poss {poss}')
            for q in poss:
                if q.within(lines):
                    # print('JB', want, q, q.char_at(lines), q.char_at(lines) == want)
                    if q.char_at(lines) == want:
                        # print(f'XXXXX')
                        # print(f'NP1 {next_pool}')
                        next_pool.add(q)
                        # print(f'NP2 {next_pool}')
            # print(f'NP {next_pool}')
        pool = next_pool.copy()
    # print(h, pool)
    return len(pool)


def p1(lines: list[str]) -> int:
    poss_heads = parse(lines)

    return sum([trailhead_score(h) for h in poss_heads])


if __name__ == "__main__":
    d = Day(10)
    lines = d.read_lines()
    print(p1(lines))
