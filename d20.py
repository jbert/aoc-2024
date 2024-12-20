from day import Day
from pt import pt, map_find
from astar import find_path
from typing import Iterable


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


def p1(lines: list[str]) -> int:
    spaces_orig, walls_orig, start, end = parse(lines)
    path = maze_solve(spaces_orig, start, end)
    if path is None:
        raise RuntimeError(f'Problem not solvable')
    normal_picos = len(list(path))
    print(start, end)
    count = 0
    for poss_cheat in possible_cheats(spaces_orig, walls_orig):
        spaces = spaces_orig.copy()
        spaces = spaces.union(poss_cheat)
        path = maze_solve(spaces, start, end)
        if path is None:
            raise RuntimeError(f'Adding spaces broke maze?')
        picos = len(list(path))
        saved_picos = normal_picos - picos
        print(f'pc {poss_cheat} picos {picos} saved {saved_picos}')
        display_cheat(lines, poss_cheat)
        if saved_picos > 100:
            count += 1
    return int(count / 2)  # We counted each cheat twice


if __name__ == "__main__":
    d = Day(20)
    lines = d.read_lines()
    print(p1(lines))
