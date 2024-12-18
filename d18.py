from day import Day
from pt import pt, pt_parse
from astar import find_path


def parse(lines: list[str]) -> list[pt]:
    return [pt_parse(l) for l in lines]


def print_map(m):
    for row in m:
        print("".join(row))


def p1(lines: list[str], arena_exit, sim_max) -> int:
    row = ['.'] * arena_size.x
    m = [row[:] for _ in range(arena_size.y)]
    incoming = parse(lines)
    for i, p in enumerate(incoming):
        if i >= sim_max:
            break
        m[p.y][p.x] = '#'

    def get_neighbours(p: pt) -> list[pt]:
        return [p for p in p.adjacent_pts_nesw() if p.within(m)
                and p.char_at(m) == '.']

    def dist(p: pt, q: pt) -> int:
        return p.sub(q).manhattan_len()

    print_map(m)
    arena_exit = arena_size - pt(1, 1)
    path = list(find_path(pt(0, 0), arena_exit, get_neighbours,
                          heuristic_cost_estimate_fnct=dist, distance_between_fnct=dist))
#    print(path)
    return len(path) - 1


if __name__ == "__main__":
    d = Day(18)
    lines = d.read_lines()
    arena_size = pt(71, 71)
    sim_max = 1024
    if d.suffix != "":
        arena_size = pt(7, 7)
        sim_max = 12

    print(p1(lines, arena_size, sim_max))
