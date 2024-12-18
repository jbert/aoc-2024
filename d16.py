from day import Day
from pt import pt, map_find, E, NESW, dir_to_char
from astar import find_path
from time import time
import sys


def parse(lines: list[str]) -> tuple[list[str], pt, pt]:
    start = map_find(lines, 'S')
    end = map_find(lines, 'E')
    if len(start) != 1 or len(end) != 1:
        raise RuntimeError(f'too many starts or ends')
    return lines, start[0], end[0]


def calc_turns(cur: pt, new: pt) -> int:
    if cur == new:
        return 0
    if cur == pt(0, 0)-new:
        return 2
    return 1


def path_cost(path: list[tuple[pt, pt]]) -> int:
    at = path[0]
    cost = 0

    for bt in path[1:]:
        cost += step_cost(at, bt)
        at = bt
    return cost


def step_cost(at: tuple[pt, pt], bt: tuple[pt, pt]) -> int:
    a, adr = at
    b, bdr = bt
    if a == b:
        cost = 1000 * calc_turns(adr, bdr)
#        print(f'{at} {bt} -> {cost}')
        return cost
    if adr != bdr:
        raise RuntimeError('turn and step in same movement')
    if a.add(adr) != b:
        raise RuntimeError('not a step')
    cost = 1
    # print(f'{at} {bt} -> {cost}')
    return cost


def guess_dist(at: tuple[pt, pt], bt: tuple[pt, pt]) -> int:
    return at[0].sub(bt[0]).manhattan_len()

# def step_cost(at, bt) -> int:
#    a, adr = at
#    b, bdr = bt
#    d = b - a
#    if d.manhattan_len() > 1:
#        raise RuntimeError(
#            f'asked for dist between [{at}] and [{bt}] d {d}')
#    ct = calc_turns(adr, bdr)
#    if not (ct == 0 or ct == 1):
#        raise RuntimeError(
#            f'asked for dist with 180 [{at}] and [{bt}] ct {ct}')
#    cs = d.manhattan_len() > 0
#    return cs + 1000*ct


def maze_solve(spaces: set[pt], start: pt, end: pt, dr: pt) -> tuple[int, list[tuple[pt, pt]]] | None:
    # A dpt is a (pt,dir) tuple

    def get_neighbours(t) -> list[tuple[pt, pt]]:
        p, dr = t
        # We could turn stand still and turn
        ns = [(p, new_dr) for new_dr in [dr.turn_left(), dr.turn_right()]]
        # We could step - if there is space
        step = p.add(dr)
        if step in spaces:
            ns.append((step, dr))
        # print(f't {t} ns {ns}')
        return ns

    paths = [find_path((start, dr), (end, edr),
                       get_neighbours,
                       heuristic_cost_estimate_fnct=guess_dist,
                       distance_between_fnct=step_cost) for edr in NESW]
    paths = [list(p) for p in paths if p is not None]
    if len(paths) == 0:
        raise RuntimeError('no paths')
   # for p in paths:
   #     print(path_cost(p))

    paths = list(sorted(paths, key=path_cost))

    best = list(paths[0])
    return path_cost(best), best


def display_seats(lines: list[str], seats: set[pt], done: set[pt]):
    for j, line in enumerate(lines):
        pline = ""
        for i, c in enumerate(line):
            p = pt(i, j)
            if p in done:
                c = 'X'
            if p in seats:
                c = 'O'
            pline += c
        print(pline)


def display_path(lines: list[str], lpath: list[tuple[pt, pt]]):
    path = {p: dr for p, dr in lpath}
#    print(lpath)
#    print(len(lpath))
    for j, line in enumerate(lines):
        pline = ""
        for i, c in enumerate(line):
            p = pt(i, j)
            dr = path.get(p, None)
            if dr is not None:
                c = dir_to_char(dr)
            pline += c
        print(pline)

# works on test cases:
# 441440 - too high
# 349168 - too high

# p2:
# 588 - too low


def find_path_containing(p: pt, spaces: set[pt], start: pt, sdr: pt, end: pt, best_cost: int) -> list[pt] | None:
    # is there a dr for this pt where:
    # cost((start, sdr), (p,dr)) + cost((p, dr), (end, any_dr))
    #    print(f'Seeking cost [{best_cost}]')
    best_costpath_to_p = maze_solve(set(spaces), start, p, sdr)
    if best_costpath_to_p is None:
        return []
    last_step = best_costpath_to_p[1][-1]

    cost_to_p = best_costpath_to_p[0]
    if cost_to_p > best_cost:
        return []

    best_costpath_from_p = maze_solve(set(spaces), p, end, last_step[1])
    if best_costpath_from_p is None:
        return []

    cost_from_p = best_costpath_from_p[0]
    if cost_to_p + cost_from_p < best_cost:
        raise RuntimeError('impossible - better in two pieces')

    def extract_path_pts(costpath: tuple[int, list[tuple[pt, pt]]]) -> list[pt]:
        return [t[0] for t in costpath[1]]

    if cost_to_p + cost_from_p == best_cost:
        return extract_path_pts(best_costpath_to_p) + extract_path_pts(best_costpath_from_p)
    return []


def p2(lines: list[str]) -> int:

    maze, start, end = parse(lines)
    spaces = set(map_find(maze, '.') + [start, end])

    best_cost_path = maze_solve(set(spaces), start, end, E)
    if best_cost_path is None:
        raise RuntimeError("Can't find")
    best_cost = best_cost_path[0]

    loops = 0
    seats = set()
    done = set()
    for i, s in enumerate(spaces):
        done.add(s)
        if s in seats:
            continue
        before = time()
        new_seats = find_path_containing(s, spaces, start, E,
                                         end, best_cost)
        if new_seats is not None and len(new_seats) > 0:
            #            print(f'new_seats {new_seats}')
            seats = seats.union(set(new_seats))
        after = time()
        # print(f'{i}/{len(spaces)} - seats {len(seats)} - {s} {after-before}')
        if loops % 100 == 0:
            display_seats(lines, set(seats), done)
        loops += 1
    display_seats(lines, set(seats), done)
    return len(seats)


def p1(lines: list[str]) -> int:
    sys.setrecursionlimit(20000)

    maze, start, end = parse(lines)
    spaces = map_find(maze, '.') + [start, end]
    # print(start, end)
    cost_path = maze_solve(set(spaces), start, end, E)
    if cost_path is None:
        raise RuntimeError("can't solve")
    cost, path = cost_path
    display_path(lines, path)
    return cost


if __name__ == "__main__":
    d = Day(16)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
