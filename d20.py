from day import Day
from pt import pt, map_find
from astar import find_path
from typing import Iterable
from time import time


def maze_solve(spaces: set[pt], start: pt, end: pt) -> Iterable[pt] | None:

    def get_neighbours(p: pt) -> list[pt]:
        return list(set(p.adjacent_pts_nesw()).intersection(spaces))

    def dist(a: pt, b: pt) -> int:
        return a.sub(b).manhattan_len()

    path = find_path(start, end,
                     get_neighbours,
                     heuristic_cost_estimate_fnct=dist,
                     distance_between_fnct=dist)
    return path


def parse(lines: list[str]) -> tuple[set[pt], set[pt], pt, pt]:
    starts = map_find(lines, 'S')
    ends = map_find(lines, 'E')
    if len(starts) != 1 or len(ends) != 1:
        raise RuntimeError(f'too many starts or ends')
    spaces = set(map_find(lines, '.') + [starts[0], ends[0]])
    walls = set(map_find(lines, '#'))
    return spaces, walls, starts[0], ends[0]


def possible_cheats(spaces, walls):
    for w1 in walls:
        n1s = set(w1.adjacent_pts_nesw())
        n1s = spaces.intersection(n1s)
        for n2 in n1s:
            yield w1, n2


def display_cheat(lines: list[str], cheat):
    for j, line in enumerate(lines):
        pline = ""
        for i, c in enumerate(line):
            p = pt(i, j)
            if p == cheat[0]:
                c = '1'
            if p == cheat[1]:
                c = '2'
            pline += c
        print(pline)


def calc_paths_from(spaces, end) -> dict[pt, list[pt] | None]:
    paths_from: dict[pt, list[pt] | None] = {}

    # set of adjacent new and done pts
    def find_adj(p: pt) -> tuple[set[pt], set[pt]]:
        adj_spaces = set(p.adjacent_pts_nesw()).intersection(spaces)
        return adj_spaces - done, adj_spaces.intersection(done)

    paths_from[end] = [end]
    done = set([end])
    fringe, wtf = find_adj(end)
    if len(wtf) > 0:
        raise RuntimeError('wtf')

    while len(fringe) > 0:
        p = fringe.pop()

        fs, qs = find_adj(p)
        fringe = fringe.union(fs)

        paths = sorted([v for v in [paths_from[q]
                                    for q in qs] if v is not None], key=lambda l: len(l))
        if len(paths) == 0:
            paths_from[p] = None
        else:
            paths_from[p] = [p] + paths[0]
        done.add(p)

    return paths_from


# 762 - too low
def p1(lines: list[str]) -> int:
    spaces, walls, start, end = parse(lines)

    print('Calculating paths...')
    before = time()
    paths_from = calc_paths_from(spaces, end)
    paths_to = calc_paths_from(spaces, start)
    for path_to in paths_to.values():
        if path_to is not None:
            path_to.reverse()
    after = time()
    print(f'Done {after-before}')

    start_to_end = paths_from[start]
    if start_to_end is None:
        raise RuntimeError(f'Problem not solvable')

    normal_picos = len(start_to_end)
    print(start, end, normal_picos)
    count = 0
    num_checked = 0
    poss_cheats = list(possible_cheats(spaces, walls))
    lpc = len(poss_cheats)
    for pc in poss_cheats:
        num_checked += 1
#        print(f'pc {num_checked}/{lpc} {pc}')

        ptcs = sorted(filter(lambda v: v is not None, [
            paths_to[p] for p in pc[0].adjacent_pts_nesw() if p in spaces]), key=lambda l: len(l))
        ptc = ptcs[0]
        if ptc is None:
            raise RuntimeError(f"can't path to cheat start")

        pfc = paths_from[pc[1]]
        if pfc is None:
            raise RuntimeError(f"can't path from cheat to end")

        if len(set(ptc).intersection(set(pfc))) != 0:
            continue
        picos = len(ptc) + len(pfc)
        saved_picos = normal_picos - picos
        if saved_picos <= 0:
            continue
#        print(f'pc {pc} picos {picos} saved {saved_picos}')
#        print(f'ptc {ptc}')
#        print(f'pfc {pfc}')
#        display_cheat(lines, pc)
        if saved_picos >= 100:
            count += 1
#            print(f'pc {pc} picos {picos} saved {saved_picos}')
#            print(f'ptc {ptc}')
#            print(f'pfc {pfc}')
#            display_cheat(lines, pc)
    return count


if __name__ == "__main__":
    d = Day(20)
    lines = d.read_lines()
    print(p1(lines))
